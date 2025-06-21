import numpy as np
import cv2 as cv
from easyocr import Reader
from rtree.index import Index


def get_ocr_reader():
    return Reader(
        ['pl'], 
        gpu=True,
        download_enabled=True
    )


def detect_text(reader, im):
    # Perform text detection
    return reader.readtext(
        im,
        decoder='beamsearch',  # Better for longer text
        beamWidth=3,           # Higher value for more accuracy (but slower)
        batch_size=1,          # Process multiple text instances at once
        workers=0,             # Use multiple CPU cores
        allowlist=None,        # No character restrictions
        blocklist=None,        # No characters to exclude
        detail=1,              # Return detailed information
        paragraph=False,        # Group text into paragraphs when possible
        min_size=55,           # Minimum text size to detect (in pixels)
        contrast_ths=0.3,      # Contrast threshold (lower for low-contrast text)
        adjust_contrast=0.5,   # Adjust contrast for better detection
        text_threshold=0.15,    # Text confidence threshold
        low_text=0.05,         # Lower text confidence threshold
        link_threshold=0.4,    # Character linking threshold
        mag_ratio=1.0,         # Image magnification ratio
        slope_ths=0.25,         # Maximum slope for text rotation
        height_ths=0.5,        # Height variation threshold
        width_ths=0.5,         # Width variation threshold
        add_margin=0.1         # Add margin around text
    )


def find_im_boxes(im, min_box_area):
    _, thresh = cv.threshold(im, 64, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    boxes = []
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if w * h > min_box_area:
            boxes.append((x, y, x+w, y+h))

    return tuple(boxes)


def merge_boxes(boxes, distance_thresh):
    box_q = list(boxes)
    boxes = []
    covered = []

    idx = Index()
    it = 0
    while box_q:
        x1, y1, x2, y2 = box_q.pop(0)
        covered_boxes = list(idx.intersection((
            x1 - distance_thresh, y1 - distance_thresh, x2 + distance_thresh, y2 + distance_thresh
        )))
        for box_idx in covered_boxes:
            if covered[box_idx]:
                continue
            covered[box_idx] = True
            b2_x1, b2_y1, b2_x2, b2_y2 = boxes[box_idx]
            x1 = min(x1, b2_x1)
            y1 = min(y1, b2_y1)
            x2 = max(x2, b2_x2)
            y2 = max(y2, b2_y2)

        idx.insert(it, (x1, y1, x2, y2))
        boxes.append((x1, y1, x2, y2))
        covered.append(False)
        it += 1

    return tuple(
        bbox
        for bbox, cov in zip(boxes, covered)
        if not cov
    )


def detect_text_in_boxes(reader, im, boxes):
    detections = []
    for x1, y1, x2, y2 in boxes:
        im_rect = im[y1:y2, x1:x2]
        for rect, text, score in detect_text(reader, im_rect):
            rect = np.array(rect, dtype=np.float32) + (x1, y1)
            detections.append((rect, text, float(score)))
    return detections
