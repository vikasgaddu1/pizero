"""
Configuration settings for the AI Vision Assistant
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
