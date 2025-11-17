"""
Main Vision Assistant class for AI Vision Assistant
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

from .config import Config
from .image import ImageOptimizer


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

    def _build_prompt(self, user_request: str = None) -> str:
        """
        Build dynamic prompt based on user request

        Args:
            user_request: Optional specific user request

        Returns:
            Tailored prompt string
        """
        if user_request:
            # Analyze user intent from their request
            request_lower = user_request.lower()

            # Medication/prescription focused
            if any(word in request_lower for word in ['prescription', 'medication', 'medicine', 'pill', 'drug', 'dosage', 'dose']):
                return """Read and analyze this medication label or prescription. Provide:
- Medication name (brand and generic)
- Dosage and strength
- Instructions for use (how often, when to take, with/without food)
- Important warnings and precautions
- Expiration date
- Active ingredients
- Any other critical safety information

Be clear, accurate, and thorough. This is safety-critical information."""

            # Food/nutrition focused
            elif any(word in request_lower for word in ['food', 'ingredients', 'nutrition', 'allergen', 'eat', 'calories']):
                return """Analyze this food product label. Provide:
- Product name and type
- Key ingredients (especially first 5)
- Allergen warnings (nuts, dairy, gluten, etc.)
- Nutritional highlights (calories, protein, sugar, etc.)
- Expiration or best-by date
- Serving size information

Focus on health and safety relevant information."""

            # Document/text reading
            elif any(word in request_lower for word in ['read', 'document', 'letter', 'text', 'form', 'paper']):
                return """Read and extract the text from this document. Provide:
- Main heading or title
- Key information and important text
- Any dates, numbers, or critical details
- Structure (sections, bullet points, etc.)

Read it clearly as if reading aloud to someone."""

            # General identification
            elif any(word in request_lower for word in ['what', 'identify', 'describe', 'tell me']):
                return f"""The user asked: "{user_request}"

Analyze this image and answer their question. Provide relevant information about:
- What you see in the image
- Key details that answer their question
- Any important context or information

Be helpful, clear, and focused on what the user asked."""

        # Default intelligent prompt if no specific request
        return """Analyze this image and provide relevant information based on what you see.

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

    def analyze_image(self, image: Image.Image, user_request: str = None) -> str:
        """
        Analyze image using Gemini API

        Args:
            image: PIL Image object
            user_request: Optional user's specific request (e.g., "read the prescription")

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

            # Build prompt based on user request
            prompt = self._build_prompt(user_request)

            if user_request:
                print(f"User requested: '{user_request}'")

            response = self.gemini_model.generate_content([prompt, optimized_image])

            description = response.text
            print(f"Analysis complete: {description[:100]}...")

            return description

        except Exception as e:
            print(f"Error analyzing image: {e}")
            return f"Sorry, I encountered an error analyzing the image: {str(e)}"

    def listen_for_keyword(self) -> str:
        """
        Listen for voice keyword and optional command

        Returns:
            Recognized text (lowercase)
        """
        with sr.Microphone(device_index=self.config.MICROPHONE_INDEX) as source:
            print("\nListening for keyword...")

            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                # Listen with longer timeout to capture full commands like "click: read the prescription"
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

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

    def process_capture_command(self, user_request: str = None):
        """Process a capture command: take photo, analyze, and speak result

        Args:
            user_request: Optional specific user request (e.g., "read the prescription")
        """
        try:
            # Give audio feedback
            self.speak("Taking picture")

            # Capture image
            image, filepath = self.capture_image()

            # Analyze image with user's request
            self.speak("Analyzing")
            description = self.analyze_image(image, user_request)

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
        print(f"Say '{self.config.KEYWORD} [request]' for specific analysis")
        print("Examples:")
        print(f"  - '{self.config.KEYWORD} read the prescription'")
        print(f"  - '{self.config.KEYWORD} what ingredients are in this'")
        print(f"  - '{self.config.KEYWORD} read this document'")
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

                    # Extract user request if present
                    # Remove the keyword and any following colons/whitespace
                    user_request = None
                    if len(text) > len(self.config.KEYWORD):
                        # Extract text after keyword
                        request_part = text[text.index(self.config.KEYWORD) + len(self.config.KEYWORD):].strip()
                        # Remove common separators like ":" or "-"
                        request_part = request_part.lstrip(':').lstrip('-').strip()
                        if request_part:
                            user_request = request_part

                    self.process_capture_command(user_request)

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
