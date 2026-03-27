"""
Build parking slot dataset from COCO annotations
Extracts 10% of the dataset for faster training iterations
"""

import os
import numpy as np
import random
from pathlib import Path

from data_loader import ParkingDatasetLoader
from preprocessor import crop_slot

# Initialize loader
loader = ParkingDatasetLoader("../datasets")

# Load training data annotations
print("[1/4] Loading dataset annotations...")
data = loader.load_annotations("train")
print(f"  Total samples in train set: {len(data)}")

# Get statistics before sampling
stats_before = loader.get_statistics("train")
print(f"  Distribution: {stats_before['occupied']} occupied, {stats_before['vacant']} vacant")

# Sample 10% of the dataset
print("\n[2/4] Sampling 10% of dataset for faster training...")
sample_size = int(0.1 * len(data))
data_sampled = random.sample(data, sample_size)
print(f"  Using {sample_size} samples (10% of {len(data)} total)")

# Extract crops for each sample
print("\n[3/4] Extracting parking slot crops...")
X = []
y = []
failed = 0

for idx, item in enumerate(data_sampled):
    if (idx + 1) % max(1, len(data_sampled) // 10) == 0:
        print(f"  Progress: {idx+1}/{len(data_sampled)}")

    slot = crop_slot(item["image_path"], item["bbox"])

    if slot is None:
        failed += 1
        continue

    X.append(slot)
    y.append(item["label"])

X = np.array(X)
y = np.array(y)

print(f"  Successfully extracted {len(X)} samples ({failed} failed)")
print(f"  Dataset shape: {X.shape}")
print(f"  Labels shape: {y.shape}")

# Verify class distribution
occupied_count = np.sum(y == 1)
vacant_count = np.sum(y == 0)
print(f"  Class distribution: {occupied_count} occupied, {vacant_count} vacant")

# Save to files
print("\n[4/4] Saving dataset...")
np.save("X_train.npy", X)
np.save("y_train.npy", y)
print(f"  Saved X_train.npy ({X.nbytes / 1e6:.1f} MB)")
print(f"  Saved y_train.npy ({y.nbytes / 1e6:.1f} MB)")

print("\n✅ Dataset building complete!")
print(f"   Ready for training: {len(X)} samples from 10% of full dataset")
