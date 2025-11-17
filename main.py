#!/usr/bin/env python3
"""
AI Vision Assistant for Raspberry Pi Zero
Captures images on voice command and describes them using Gemini API
"""

import os
import io
import time
from datetime import datetime
from pathlib import Path
import speech_recognition as sr
import pyttsx3
from picamera2 import Picamera2
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
class Config:
    """Configuration settings for the AI Vision Assistant"""
    
    # API Settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'  # Fast and efficient for Pi Zero
    
    # Image Settings
    MAX_IMAGE_SIZE = 1024  # Maximum dimension (width or height)
    JPEG_QUALITY = 85  # JPEG compression quality (1-100)
    IMAGE_DIR = 'captured_images'
    
    # Camera Settings
    CAMERA_RESOLUTION = (1920, 1080)  # Full HD
    CAMERA_WARMUP_TIME = 2  # Seconds to let camera adjust
    
    # Voice Recognition Settings
    KEYWORD = 'click'  # Trigger word
    EXIT_KEYWORDS = ['exit', 'quit', 'stop']
    MICROPHONE_INDEX = None  # None = default, or specify index
    
    # Text-to-Speech Settings
    TTS_RATE = 150  # Words per minute
    TTS_VOLUME = 0.9  # Volume level (0.0 to 1.0)


class ImageOptimizer:
    """Handles image optimization for efficient API usage"""
    
    @staticmethod
    def optimize_image(image: Image.Image, max_size: int = 1024, quality: int = 85) -> bytes:
        """
        Optimize image by resizing and compressing
        
        Args:
            image: PIL Image object
            max_size: Maximum dimension (width or height)
            quality: JPEG quality (1-100)
            
        Returns:
            Optimized image as bytes
        """
        # Calculate new size maintaining aspect ratio
        width, height = image.size
        if width > max_size or height > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary (remove alpha channel)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        
        # Compress to JPEG
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        
        return buffer.getvalue()


class VisionAssistant:
    """Main application class for AI Vision Assistant"""
    
    def __init__(self, config: Config):
        """Initialize the vision assistant"""
        self.config = config
        self.camera = None
        self.recognizer = sr.Recognizer()
        self.tts_engine = None
        self.gemini_model = None
        
        # Create image directory
        Path(config.IMAGE_DIR).mkdir(exist_ok=True)
        
        # Initialize components
        self._setup_camera()
        self._setup_tts()
        self._setup_gemini()
        
    def _setup_camera(self):
        """Initialize Raspberry Pi Camera"""
        try:
            print("Initializing camera...")
            self.camera = Picamera2()
            
            # Configure camera
            camera_config = self.camera.create_still_configuration(
                main={"size": self.config.CAMERA_RESOLUTION}
            )
            self.camera.configure(camera_config)
            self.camera.start()
            
            # Allow camera to warm up
            print(f"Camera warming up for {self.config.CAMERA_WARMUP_TIME} seconds...")
            time.sleep(self.config.CAMERA_WARMUP_TIME)
            
            print("Camera ready!")
        except Exception as e:
            print(f"Error initializing camera: {e}")
            raise
    
    def _setup_tts(self):
        """Initialize text-to-speech engine"""
        try:
            print("Initializing text-to-speech...")
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.config.TTS_RATE)
            self.tts_engine.setProperty('volume', self.config.TTS_VOLUME)
            print("Text-to-speech ready!")
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            raise
    
    def _setup_gemini(self):
        """Initialize Gemini API"""
        try:
            print("Initializing Gemini API...")
            if not self.config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            genai.configure(api_key=self.config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(self.config.GEMINI_MODEL)
            print("Gemini API ready!")
        except Exception as e:
            print(f"Error initializing Gemini API: {e}")
            raise
    
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"Speaking: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def capture_image(self) -> tuple[Image.Image, str]:
        """
        Capture an image from the camera
        
        Returns:
            Tuple of (PIL Image, filepath)
        """
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.config.IMAGE_DIR, f"capture_{timestamp}.jpg")
            
            # Capture image
            print("Capturing image...")
            self.camera.capture_file(filepath)
            
            # Load image as PIL Image
            image = Image.open(filepath)
            
            print(f"Image captured: {filepath}")
            return image, filepath
            
        except Exception as e:
            print(f"Error capturing image: {e}")
            raise
    
    def analyze_image(self, image: Image.Image) -> str:
        """
        Analyze image using Gemini API
        
        Args:
            image: PIL Image object
            
        Returns:
            Description text from Gemini
        """
        try:
            print("Optimizing image for analysis...")
            
            # Optimize image
            optimized_bytes = ImageOptimizer.optimize_image(
                image,
                max_size=self.config.MAX_IMAGE_SIZE,
                quality=self.config.JPEG_QUALITY
            )
            
            # Convert bytes to PIL Image for Gemini
            optimized_image = Image.open(io.BytesIO(optimized_bytes))

            # Calculate original size for comparison
            original_buffer = io.BytesIO()
            image.save(original_buffer, format='JPEG')
            original_size = len(original_buffer.getvalue())
            optimized_size = len(optimized_bytes)

            reduction_percent = ((original_size - optimized_size) / original_size * 100) if original_size > 0 else 0
            print(f"Image optimized: {optimized_size / 1024:.1f} KB (reduced by {reduction_percent:.1f}%)")
            
            # Generate description
            print("Analyzing image with Gemini...")
            prompt = """Analyze this image and provide relevant information based on what you see.

MEDICATION LABELS - If this is a medication bottle, prescription label, pill bottle, or pharmaceutical product:
- Medication name (brand and generic if visible)
- Dosage and strength (e.g., "500 mg", "10 ml")
- Instructions for use (e.g., "Take twice daily with food")
- Important warnings or precautions
- Expiration date if visible
- Active ingredients
- Prescription number if visible
- Any critical safety information
Format this clearly and read it in a way that's easy to understand when spoken aloud.

FOOD LABELS - If this is food packaging or nutrition label:
- Product name and type
- Key ingredients
- Nutritional highlights
- Allergen warnings
- Expiration or best-by date
- Serving information

DOCUMENTS/TEXT - If this contains text, forms, or documents:
- Main heading or title
- Key information or important text
- Any dates, numbers, or critical details
- Purpose of the document

GENERAL OBJECTS - For other items:
- What the object is
- Its purpose or function
- Notable features or condition
- Any text, labels, or markings visible
- Relevant context or usage information

IMPORTANT: Be concise, clear, and prioritize safety-critical information first (especially for medications). Speak naturally as if helping someone who cannot see the image."""
            
            response = self.gemini_model.generate_content([prompt, optimized_image])
            
            description = response.text
            print(f"Analysis complete: {description[:100]}...")
            
            return description
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"Sorry, I encountered an error analyzing the image: {str(e)}"
    
    def listen_for_keyword(self) -> str:
        """
        Listen for voice keyword
        
        Returns:
            Recognized text (lowercase)
        """
        with sr.Microphone(device_index=self.config.MICROPHONE_INDEX) as source:
            print("\nListening for keyword...")
            
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: '{text}'")
                
                return text
                
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                return ""
    
    def process_capture_command(self):
        """Process a capture command: take photo, analyze, and speak result"""
        try:
            # Give audio feedback
            self.speak("Taking picture")
            
            # Capture image
            image, filepath = self.capture_image()
            
            # Analyze image
            self.speak("Analyzing")
            description = self.analyze_image(image)
            
            # Speak result
            self.speak(description)
            
        except Exception as e:
            error_msg = "Sorry, I encountered an error processing the image"
            print(f"Error in process_capture_command: {e}")
            self.speak(error_msg)
    
    def run(self):
        """Main application loop"""
        print("\n" + "="*50)
        print("AI Vision Assistant Started")
        print("="*50)
        print(f"Say '{self.config.KEYWORD}' to capture and analyze an image")
        print(f"Say 'exit' or 'quit' to stop")
        print("="*50 + "\n")
        
        self.speak("AI Vision Assistant ready")
        
        try:
            while True:
                # Listen for keyword
                text = self.listen_for_keyword()
                
                # Check for exit command
                if any(exit_word in text for exit_word in self.config.EXIT_KEYWORDS):
                    print("Exit command received")
                    self.speak("Goodbye")
                    break
                
                # Check for trigger keyword
                if self.config.KEYWORD in text:
                    print(f"\n>>> Keyword '{self.config.KEYWORD}' detected! <<<\n")
                    self.process_capture_command()
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nCleaning up...")
        
        if self.camera:
            try:
                self.camera.stop()
                print("Camera stopped")
            except:
                pass
        
        if self.tts_engine:
            try:
                self.tts_engine.stop()
                print("TTS engine stopped")
            except:
                pass
        
        print("Cleanup complete")


def main():
    """Main entry point"""
    try:
        # Create configuration
        config = Config()
        
        # Create and run assistant
        assistant = VisionAssistant(config)
        assistant.run()
        
    except Exception as e:
        print(f"\nFatal error: {e}")
        print("\nPlease check:")
        print("1. Camera is properly connected")
        print("2. Audio devices are working")
        print("3. GEMINI_API_KEY is set in .env file")
        print("4. Internet connection is active")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
