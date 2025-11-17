#!/usr/bin/env python3
"""
Command-line interface for AI Vision Assistant
"""

from .config import Config
from .assistant import VisionAssistant


def main():
    """Main entry point for the CLI"""
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
