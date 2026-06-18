"""
Image compression utilities.

Automatically compress and resize uploaded images to ensure fast load times
without quality loss that's visible to the human eye.

Rules:
  - Max dimension: 1920px on longest side (preserves aspect ratio)
  - JPEG quality: 82 (visually lossless, ~60-75% smaller than raw)
  - PNG files are converted to JPEG if they don't need transparency
  - WebP is used when the original is already WebP
  - Files under 100 KB are left untouched (already small enough)
  - Video files and non-image fields are ignored

Usage:
    from website.image_utils import compress_image_field
    compress_image_field(instance.featured_image)
"""
import io
import os

from PIL import Image

# Maximum longest dimension in pixels (1200px is optimal for Facebook/WhatsApp og:image)
MAX_DIMENSION = 1200

# JPEG quality (1-95). 82 gives excellent quality at ~60% smaller file size.
JPEG_QUALITY = 82

# Files smaller than this (bytes) are left untouched.
MIN_SIZE_TO_COMPRESS = 100 * 1024  # 100 KB


def compress_image_field(image_field):
    """
    Compress and resize an ImageField's uploaded file in-place using Django's storage API.

    This works for both local storage and cloud storage backends (like AWS S3).
    Returns True if the image was recompressed, False if skipped.
    """
    if not image_field or not image_field.name:
        return False

    try:
        # Avoid compressing very small files
        try:
            if image_field.size < MIN_SIZE_TO_COMPRESS:
                return False
        except (ValueError, AttributeError, OSError):
            return False

        # Open the image file using Django's storage API
        storage = image_field.storage
        try:
            with storage.open(image_field.name, 'rb') as f:
                img_data = f.read()
        except Exception:
            return False

        # Read into PIL
        with Image.open(io.BytesIO(img_data)) as img:
            original_format = (img.format or 'JPEG').upper()
            original_mode = img.mode

            # Determine output format
            if original_format == 'WEBP':
                out_format = 'WEBP'
                save_kwargs = {'quality': JPEG_QUALITY, 'method': 6}
            elif original_format == 'PNG' and _has_transparency(img):
                out_format = 'PNG'
                save_kwargs = {'optimize': True}
            else:
                out_format = 'JPEG'
                save_kwargs = {'quality': JPEG_QUALITY, 'optimize': True}

            # Convert mode if needed
            if out_format == 'JPEG' and original_mode not in ('RGB', 'L'):
                img = img.convert('RGB')

            # Resize if too large
            w, h = img.size
            longest = max(w, h)
            if longest > MAX_DIMENSION:
                ratio = MAX_DIMENSION / longest
                new_size = (int(w * ratio), int(h * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            # Save to buffer
            buf = io.BytesIO()
            img.save(buf, format=out_format, **save_kwargs)
            compressed_bytes = buf.getvalue()

            # Only overwrite if it actually saved space
            if len(compressed_bytes) < len(img_data):
                from django.core.files.base import ContentFile
                storage.delete(image_field.name)
                storage.save(image_field.name, ContentFile(compressed_bytes))
                return True

    except Exception:
        pass  # Never crash the upload flow

    return False


def _has_transparency(img):
    """Return True if the image has a meaningful alpha channel."""
    if img.mode == 'RGBA':
        extrema = img.getextrema()
        if extrema[3][0] < 255:  # alpha min < 255
            return True
    elif img.mode == 'P' and 'transparency' in img.info:
        return True
    return False
