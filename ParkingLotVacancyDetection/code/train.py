"""
Train ResNet18 model on parking dataset
Uses 10% of dataset for faster iterations
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import models
import os
import sys

# ==================== CONFIGURATION ====================
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
MODEL_SAVE_PATH = "../module4_deep_learning/resnet18_parking.pth"

print("=" * 60)
print("  ResNet18 Parking Space Detector - Training")
print("  Using 10% of dataset for fast iterations")
print("=" * 60)

# ==================== LOAD DATASET ====================
print("\n[1/5] Loading dataset...")
try:
    X_train = np.load("X_train.npy")
    y_train = np.load("y_train.npy")
    print(f"  ✓ Loaded X_train: {X_train.shape}")
    print(f"  ✓ Loaded y_train: {y_train.shape}")
except FileNotFoundError:
    print("  ✗ Error: X_train.npy or y_train.npy not found!")
    print("  Run build_slot_dataset.py first: python code/build_slot_dataset.py")
    sys.exit(1)

# Verify dataset
occupied = np.sum(y_train == 1)
vacant = np.sum(y_train == 0)
print(f"  Class distribution: {occupied} occupied, {vacant} vacant")

# ==================== PREPARE TENSORS ====================
print("\n[2/5] Preparing data...")
# Adjust labels if needed (assuming original are 0 and 1)
y_train = np.array(y_train, dtype=np.int64)

# Convert to torch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)

# Rearrange to (N, C, H, W) if needed
if len(X_train_tensor.shape) == 4 and X_train_tensor.shape[1] != 3:
    # Assume (N, H, W, C) format, convert to (N, C, H, W)
    X_train_tensor = X_train_tensor.permute(0, 3, 1, 2)

# Normalize to [0, 1]
X_train_tensor = X_train_tensor / 255.0

y_train_tensor = torch.tensor(y_train, dtype=torch.long)

print(f"  ✓ X_train tensor: {X_train_tensor.shape}")
print(f"  ✓ y_train tensor: {y_train_tensor.shape}")
print(f"  ✓ Value range: [{X_train_tensor.min():.2f}, {X_train_tensor.max():.2f}]")

# Create dataset and dataloader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
print(f"  ✓ DataLoader created: {len(train_loader)} batches of size {BATCH_SIZE}")

# ==================== LOAD MODEL ====================
print("\n[3/5] Loading model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"  ✓ Device: {device}")

# Load pre-trained ResNet18
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, 2)  # Binary classification: occupied/vacant
model.to(device)
print(f"  ✓ ResNet18 loaded with 2-class head (occupied/vacant)")

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
print(f"  ✓ Optimizer: Adam (lr={LEARNING_RATE})")
print(f"  ✓ Loss: CrossEntropyLoss")

# ==================== TRAINING LOOP ====================
print(f"\n[4/5] Training for {NUM_EPOCHS} epochs...")
print("-" * 60)

best_loss = float('inf')
total_samples_processed = 0

for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0
    num_batches = 0
    epoch_samples = 0

    try:
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)

            # Forward pass
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward pass
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            num_batches += 1
            epoch_samples += inputs.shape[0]

            # Progress every 20 batches
            if (batch_idx + 1) % 20 == 0:
                print(f"  Epoch {epoch+1}/{NUM_EPOCHS} | "
                      f"Batch {batch_idx+1}/{len(train_loader)} | "
                      f"Loss: {loss.item():.4f}")

    except KeyboardInterrupt:
        print("\n\n✗ Training interrupted by user!")
        print("  Model not saved.")
        sys.exit(1)

    # End of epoch
    avg_loss = running_loss / num_batches if num_batches > 0 else 0
    total_samples_processed += epoch_samples
    
    if avg_loss < best_loss:
        best_loss = avg_loss
        marker = " ← Best"
    else:
        marker = ""

    print(f"  ✓ Epoch {epoch+1} complete | "
          f"Avg Loss: {avg_loss:.4f}{marker} | "
          f"Samples: {epoch_samples}")

print("-" * 60)

# ==================== SAVE MODEL ====================
print(f"\n[5/5] Saving model...")
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
torch.save(model.state_dict(), MODEL_SAVE_PATH)
file_size_mb = os.path.getsize(MODEL_SAVE_PATH) / 1e6
print(f"  ✓ Model saved: {MODEL_SAVE_PATH}")
print(f"  ✓ File size: {file_size_mb:.1f} MB")

# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("  ✅ TRAINING COMPLETE!")
print("=" * 60)
print(f"Samples trained on:    {total_samples_processed} (from 10% of full dataset)")
print(f"Epochs:                {NUM_EPOCHS}")
print(f"Final loss:            {avg_loss:.4f}")
print(f"Best loss:             {best_loss:.4f}")
print(f"Model saved to:        {MODEL_SAVE_PATH}")
print(f"Model ready for inference via app.py")
print("=" * 60)
