from easyocr import Reader


def get_ocr_reader():
    return Reader(
        ['pl', 'en'], 
        gpu=True,  # Enable GPU if available for faster processing
        model_storage_directory='~/model_storage',
        download_enabled=True
    )


def detect_text(reader, im):
    # Perform text detection
    return reader.readtext(
        im,
        decoder='beamsearch',  # Better for longer text
        beamWidth=5,           # Higher value for more accuracy (but slower)
        batch_size=10,         # Process multiple text instances at once
        workers=4,             # Use multiple CPU cores
        allowlist=None,        # No character restrictions
        blocklist=None,        # No characters to exclude
        detail=1,              # Return detailed information
        # paragraph=True,        # Group text into paragraphs when possible
        min_size=5,           # Minimum text size to detect (in pixels)
        contrast_ths=0.3,      # Contrast threshold (lower for low-contrast text)
        adjust_contrast=0.7,   # Adjust contrast for better detection
        text_threshold=0.15,    # Text confidence threshold
        low_text=0.05,         # Lower text confidence threshold
        link_threshold=0.4,    # Character linking threshold
        mag_ratio=2.0,         # Image magnification ratio
        slope_ths=0.25,         # Maximum slope for text rotation
        height_ths=0.5,        # Height variation threshold
        width_ths=0.5,         # Width variation threshold
        add_margin=0.1         # Add margin around text
    )
