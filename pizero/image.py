"""
Image optimization utilities for the AI Vision Assistant
"""

import io
from PIL import Image


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
