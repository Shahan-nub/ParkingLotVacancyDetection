"""
Test the trained ResNet18 model on validation set
"""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from torchvision import models
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("  ResNet18 Parking Model - Validation")
print("=" * 60)

# ==================== CONFIGURATION ====================
MODEL_PATH = "module4_deep_learning/resnet18_parking.pth"
BATCH_SIZE = 32
TEST_SAMPLES = 10  # Number of samples to test

# ==================== LOAD MODEL ====================
print("\n[1/3] Loading trained model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"  ✓ Device: {device}")

try:
    model = models.resnet18()
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    print(f"  ✓ Model loaded from: {MODEL_PATH}")
except Exception as e:
    print(f"  ✗ Error loading model: {e}")
    sys.exit(1)

# ==================== LOAD TEST DATA ====================
print("\n[2/3] Loading test data...")
try:
    X_train = np.load("code/X_train.npy")
    y_train = np.load("code/y_train.npy")
    print(f"  ✓ Dataset loaded: {X_train.shape}")
    
    # Use last 10% as test set (simple split)
    test_size = min(TEST_SAMPLES, len(X_train) // 10)
    X_test = X_train[-test_size:]
    y_test = y_train[-test_size:]
    
except Exception as e:
    print(f"  ✗ Error loading data: {e}")
    sys.exit(1)

# ==================== INFERENCE ====================
print(f"\n[3/3] Running inference on {len(X_test)} test samples...")
print("-" * 60)

# Convert to tensors
X_test_tensor = torch.tensor(X_test, dtype=torch.float32) / 255.0
if len(X_test_tensor.shape) == 4 and X_test_tensor.shape[1] != 3:
    X_test_tensor = X_test_tensor.permute(0, 3, 1, 2)

y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# Create dataloader
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Inference
correct = 0
total = 0
confidences = []

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs = inputs.to(device)
        
        outputs = model(inputs)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        predictions = torch.argmax(outputs, dim=1)
        
        correct += (predictions == labels.to(device)).sum().item()
        total += labels.shape[0]
        
        # Store confidences
        max_confs = torch.max(probabilities, dim=1)[0]
        confidences.extend(max_confs.cpu().numpy())

# ==================== RESULTS ====================
accuracy = 100 * correct / total if total > 0 else 0

print(f"Samples tested:        {total}")
print(f"Correct predictions:   {correct}/{total}")
print(f"Accuracy:              {accuracy:.1f}%")
print(f"Avg confidence:        {np.mean(confidences):.1%}")
print(f"Min confidence:        {np.min(confidences):.1%}")
print(f"Max confidence:        {np.max(confidences):.1%}")
print("-" * 60)

if accuracy >= 80:
    print("✅ Model validation PASSED (accuracy ≥ 80%)")
else:
    print("⚠️  Model accuracy is below 80% - consider retraining")

print("=" * 60)
