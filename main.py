#!/usr/bin/env python3
"""
AI Vision Assistant for Raspberry Pi Zero
Backward compatibility wrapper - imports from the pizero package

This file exists for backward compatibility with existing deployments.
For new code, import from the pizero package directly:
    from pizero import Config, VisionAssistant, ImageOptimizer
"""

# Import everything from the package for backward compatibility
from pizero import Config, ImageOptimizer, VisionAssistant, main

# Re-export for backward compatibility
__all__ = ["Config", "ImageOptimizer", "VisionAssistant", "main"]

if __name__ == "__main__":
    exit(main())
