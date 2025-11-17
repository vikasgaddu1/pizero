"""
AI Vision Assistant for Raspberry Pi Zero
Captures images on voice command and describes them using Gemini API
"""

from .config import Config
from .image import ImageOptimizer
from .assistant import VisionAssistant
from .cli import main

__version__ = "1.0.0"
__all__ = ["Config", "ImageOptimizer", "VisionAssistant", "main"]
