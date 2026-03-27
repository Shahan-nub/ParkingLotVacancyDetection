"""
Parking space preprocessor
Crops individual parking slots from images using bounding boxes
"""

import cv2
import numpy as np
from pathlib import Path


def crop_slot(image_path: str, bbox: list, target_size: int = 64) -> np.ndarray:
    """
    Crop a parking slot from an image and resize to target size
    
    Args:
        image_path: Path to image file
        bbox: Bounding box [x, y, width, height] in COCO format
        target_size: Target output size (default 64x64)
        
    Returns:
        Cropped and resized image as numpy array, or None if error
    """
    try:
        # Read image
        if not Path(image_path).exists():
            print(f"Image not found: {image_path}")
            return None

        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            return None

        # Extract bounding box
        x, y, w, h = [int(v) for v in bbox]

        # Crop the region
        crop = image[y:y+h, x:x+w]

        if crop.size == 0:
            print(f"Empty crop for {image_path} with bbox {bbox}")
            return None

        # Resize to target size
        resized = cv2.resize(crop, (target_size, target_size))

        return resized

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def preprocess_batch(images: np.ndarray) -> np.ndarray:
    """
    Preprocess a batch of images for model input
    
    Args:
        images: Array of images (N, H, W, C) in BGR format, values 0-255
        
    Returns:
        Preprocessed images (N, C, H, W) normalized to [0, 1]
    """
    # Convert BGR to RGB
    images = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
    
    # Normalize to [0, 1]
    images = images.astype(np.float32) / 255.0
    
    # Rearrange to (N, C, H, W) for PyTorch
    images = np.transpose(images, (0, 3, 1, 2))
    
    return images


if __name__ == "__main__":
    # Test preprocessing
    test_bbox = [10, 10, 64, 64]
    test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    
    # This would crop but file doesn't exist, so just test the logic
    print("Preprocessor module loaded successfully")
