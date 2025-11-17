# AI Vision Assistant - Raspberry Pi Zero Project

## Project Overview
A voice-activated AI vision system that captures images when triggered by a keyword with optional custom requests (e.g., "click read the prescription"), intelligently analyzes them using Google's Gemini API with dynamic prompt generation, and speaks the description aloud. The system adapts its analysis based on both the user's spoken request and the image content, automatically detecting medication labels, food packaging, documents, or general objects and providing relevant information accordingly.

## Hardware Requirements

### Components
1. **Raspberry Pi Zero W** (or Pi Zero 2 W for better performance)
2. **Raspberry Pi Camera Module** (V2 or HQ Camera)
3. **RASPIAUDIO Audio DAC Hat Sound Card**
4. **USB Microphone** (if Audio DAC doesn't have built-in mic)
5. **Speaker** connected to Audio DAC
6. **MicroSD Card** (16GB+ recommended)
7. **Power Supply** (5V 2.5A recommended)

### Hardware Setup

#### Camera Connection
1. Connect the Pi Camera ribbon cable to the CSI port on Pi Zero
2. Ensure the blue side faces the Ethernet port side

#### Audio DAC Connection
1. Mount RASPIAUDIO DAC Hat on Pi Zero GPIO pins
2. Connect speaker to the 3.5mm jack or terminal blocks
3. Connect microphone to the mic input (or use USB mic)

## Software Requirements

### System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-picamera2 portaudio19-dev python3-pyaudio
sudo apt-get install -y flac espeak alsa-utils
```

### Python Libraries
```bash
pip3 install --break-system-packages google-generativeai pillow SpeechRecognition pyttsx3 python-dotenv
```

### Configuration

#### Enable Camera
```bash
sudo raspi-config
# Navigate to Interface Options -> Camera -> Enable
```

#### Test Audio DAC
```bash
# Test speaker output
speaker-test -t wav -c 2

# Test microphone
arecord -D plughw:1,0 -d 5 test.wav
aplay test.wav
```

## Features

### Core Functionality
- **Dynamic Voice Activation**: Listens for keyword "click" with optional custom requests
  - Basic: "click" - automatically detects and analyzes content
  - Custom: "click read the prescription" - tailored analysis based on your request
  - Examples: "click what ingredients", "click read this document", "click what is this"
- **Image Capture**: Takes high-quality photos using Pi Camera
- **Image Optimization**: Compresses and resizes images for efficient API usage
- **Intelligent AI Analysis**: Uses Gemini Vision API with dynamic prompt generation:
  - Adapts based on user's spoken request AND image content
  - **Medication Labels**: Reads drug names, dosages, warnings, expiration dates, and instructions
  - **Food Labels**: Identifies ingredients, nutrition info, and allergen warnings
  - **Documents**: Extracts key text, dates, and important information
  - **General Objects**: Provides relevant descriptions and context
- **Voice Output**: Speaks the analysis results through connected speaker
- **Safety Priority**: Prioritizes critical information like medication warnings and dosages
- **Low Resource Usage**: Optimized for Pi Zero's limited hardware

### Image Optimization
- Automatic resizing to 1024px max dimension
- JPEG compression (quality: 85)
- Typically reduces file size by 70-80%
- Maintains good quality for AI analysis

## Project Structure

```
ai-vision-assistant/
├── main.py                 # Main application
├── config.py              # Configuration settings
├── .env                   # API keys (create this)
├── requirements.txt       # Python dependencies
├── PROJECT_README.md      # This file
└── captured_images/       # Image storage (auto-created)
```

## Setup Instructions

### 1. Clone/Create Project
```bash
mkdir -p ~/ai-vision-assistant
cd ~/ai-vision-assistant
```

### 2. Create .env File
```bash
nano .env
```

Add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Install Dependencies
```bash
pip3 install --break-system-packages -r requirements.txt
```

### 4. Run the Application
```bash
python3 main.py
```

## Usage

1. Start the program: `python3 main.py`
2. Wait for "Listening for keyword..." message
3. Say "click" clearly into the microphone
4. Camera will capture an image
5. AI will analyze and speak the description
6. System returns to listening mode

### Voice Commands
- **"click"** - Capture and analyze image
- **"exit"** or **"quit"** - Stop the program

## Troubleshooting

### Camera Issues
```bash
# Check if camera is detected
vcgencmd get_camera

# Test camera
libcamera-hello
```

### Audio Issues
```bash
# List audio devices
aplay -l
arecord -l

# Adjust volume
alsamixer
```

### Microphone Not Working
```bash
# Check if microphone is detected
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### API Errors
- Verify API key in .env file
- Check internet connection
- Ensure Gemini API is enabled in Google Cloud Console
- Check API quota limits

### Performance Tips
- Use Pi Zero 2 W for better performance
- Reduce image size if analysis is too slow
- Consider using swap file for memory-intensive operations

## API Costs

### Gemini API Pricing (as of 2024)
- **Free Tier**: 60 requests per minute
- **Gemini 1.5 Flash**: Best for this use case (fast and free tier)
- **Image Input**: Included in free tier for moderate usage

Monitor usage at: https://console.cloud.google.com

## Future Enhancements

- [ ] Add continuous listening mode
- [ ] Support multiple keywords for different actions
- [ ] Save analysis results to log file
- [ ] Add web interface for remote triggering
- [ ] Support video analysis
- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Battery power optimization
- [ ] LED indicators for status
- [ ] Cloud storage integration

## Security Considerations

- Keep .env file secure and never commit to Git
- Use environment variables for sensitive data
- Consider implementing rate limiting
- Monitor API usage regularly
- Secure your Pi with strong passwords

## License
MIT License - Feel free to modify and distribute

## Credits
- Google Gemini API for vision analysis
- Raspberry Pi Foundation
- RASPIAUDIO for the Audio DAC Hat

## Support
For issues and questions:
- Gemini API: https://ai.google.dev/docs
- Raspberry Pi Camera: https://www.raspberrypi.com/documentation/
- RASPIAUDIO: https://raspiaudio.com/

---
**Note**: This project requires internet connectivity for the Gemini API. Ensure your Pi Zero W is connected to WiFi.
