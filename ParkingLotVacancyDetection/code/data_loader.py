"""
Custom data loader for parking datasets from Roboflow
Loads annotations and images from COCO format
"""

import json
import os
from pathlib import Path


class ParkingDatasetLoader:
    """Loads parking dataset from directory with COCO annotations"""

    def __init__(self, dataset_root: str):
        """
        Args:
            dataset_root: Path to dataset folder containing train/valid/test subdirectories
        """
        self.dataset_root = Path(dataset_root)

    def load_annotations(self, split: str = "train"):
        """
        Load annotations from COCO JSON file
        
        Args:
            split: 'train', 'valid', or 'test'
            
        Returns:
            List of items with keys: image_path, bbox, label, image_id
        """
        split_dir = self.dataset_root / split
        annotations_file = split_dir / "_annotations.coco.json"

        if not annotations_file.exists():
            raise FileNotFoundError(f"Annotations file not found: {annotations_file}")

        with open(annotations_file, 'r') as f:
            coco_data = json.load(f)

        # Build lookup dictionaries
        images_by_id = {img['id']: img for img in coco_data.get('images', [])}
        categories = {cat['id']: cat['name'] for cat in coco_data.get('categories', [])}

        # Extract items
        items = []
        for annotation in coco_data.get('annotations', []):
            image_id = annotation['image_id']
            if image_id not in images_by_id:
                continue

            image_info = images_by_id[image_id]
            image_path = split_dir / image_info['file_name']

            bbox = annotation['bbox']  # [x, y, width, height]
            category_id = annotation['category_id']
            category_name = categories.get(category_id, 'unknown')

            # Convert category name to label (0 = vacant, 1 = occupied)
            label = 1 if 'occupied' in category_name.lower() else 0

            items.append({
                'image_path': str(image_path),
                'bbox': bbox,
                'label': label,
                'image_id': image_id,
                'category': category_name
            })

        return items

    def get_statistics(self, split: str = "train"):
        """Get dataset statistics"""
        items = self.load_annotations(split)
        occupied = sum(1 for item in items if item['label'] == 1)
        vacant = sum(1 for item in items if item['label'] == 0)
        return {
            'total': len(items),
            'occupied': occupied,
            'vacant': vacant
        }


if __name__ == "__main__":
    loader = ParkingDatasetLoader("../datasets")
    stats = loader.get_statistics("train")
    print(f"Dataset statistics: {stats}")
