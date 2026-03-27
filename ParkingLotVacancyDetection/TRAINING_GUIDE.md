# 🚀 Parking Space Detector - Training Pipeline

## Quick Start (Train with 10% of Dataset)

This pipeline trains ResNet18 on **10% of the full dataset** for faster iterations.

### Step 1: Build Dataset (10% Sample)
```bash
cd code
python build_slot_dataset.py
```

**What happens:**
- Loads annotations from `datasets/train/_annotations.coco.json`
- Samples 10% of the dataset
- Extracts parking slot crops from images
- Saves `X_train.npy` and `y_train.npy` (~10% of full dataset)

**Expected output:**
```
[1/4] Loading dataset annotations...
  Total samples in train set: 49785
  Distribution: ... occupied, ... vacant

[2/4] Sampling 10% of dataset for faster training...
  Using ~4978 samples (10% of 49785 total)

[3/4] Extracting parking slot crops...
  Successfully extracted ~4978 samples

[4/4] Saving dataset...
  Ready for training: ~4978 samples from 10% of full dataset
```

### Step 2: Train Model
```bash
python train.py
```

**What happens:**
- Loads X_train.npy and y_train.npy (10% of dataset)
- Creates ResNet18 model
- Trains for 10 epochs with batch size 32
- Saves to `module4_deep_learning/resnet18_parking.pth`

**Expected output:**
```
  ResNet18 Parking Space Detector - Training
  Using 10% of dataset for fast iterations

[1/5] Loading dataset...
  ✓ Loaded X_train: (4978, 64, 64, 3)
  ✓ Loaded y_train: (4978,)

[2/5] Preparing data...
  ✓ DataLoader created: 156 batches of size 32

[3/5] Loading model...
  ✓ Device: cuda (or cpu)

[4/5] Training for 10 epochs...
  Epoch 1/10 | Batch 20/156 | Loss: 0.5234
  ✓ Epoch 1 complete | Avg Loss: 0.3421
  ...
  ✓ Epoch 10 complete | Avg Loss: 0.0891

[5/5] Saving model...
  ✓ Model saved: ../module4_deep_learning/resnet18_parking.pth
  ✓ File size: 43.0 MB

  ✅ TRAINING COMPLETE!
```

### Step 3: Validate Model (Optional)
```bash
cd ..
python test_trained_model.py
```

**What happens:**
- Loads trained model
- Tests on validation samples
- Shows accuracy and confidence metrics

---

## Dataset Information

### Full Dataset
- **Total samples:** 49,785 parking space images
- **Source:** Roboflow parking space detection dataset
- **Format:** COCO JSON annotations
- **Classes:** Occupied (1) / Vacant (0)
- **Location:** `datasets/train/`, `datasets/valid/`, `datasets/test/`

### 10% Subset (Used for Training)
- **Samples:** ~4,978 parking spaces (10% sample)
- **Purpose:** Faster training iterations for development and experimentation
- **Training time:** ~2-5 minutes on GPU, ~20-30 minutes on CPU
- **Model quality:** Comparable to full dataset training

---

## Training Configuration

Edit `code/train.py` to customize:
```python
BATCH_SIZE = 32          # Batch size for training
NUM_EPOCHS = 10          # Number of training epochs
LEARNING_RATE = 0.001    # Adam optimizer learning rate
```

---

## Output Files

After training completes, you'll have:

```
module4_deep_learning/
├── resnet18_parking.pth        # Trained model weights (43 MB)
├── inference_engine.py         # Inference code
└── README.md

code/
├── X_train.npy                 # Training images (10% of full)
├── y_train.npy                 # Training labels (10% of full)
└── *.py                        # Training scripts
```

---

## Using the Trained Model

The trained model is automatically loaded by the web app:

```bash
streamlit run app.py
```

The model will be used for:
- Real-time parking space classification
- Multi-slot occupancy analysis
- Heatmap generation

---

## Troubleshooting

### Error: "FileNotFoundError: X_train.npy"
**Solution:** Run `build_slot_dataset.py` first

### Error: "Cannot open video/image" in build_slot_dataset.py
**Solution:** Verify `datasets/` folder structure:
```
datasets/
├── train/
│   ├── _annotations.coco.json
│   ├── image_001.jpg
│   ├── image_002.jpg
│   └── ...
├── valid/
└── test/
```

### Training very slow (CPU)
**Solution:** 
- Use GPU if available (10-50x faster)
- Reduce `NUM_EPOCHS` temporarily for testing
- Reduce `BATCH_SIZE` to 16 if out of memory

### Model accuracy too low
**Solution:**
- Use full 100% dataset: modify `build_slot_dataset.py` line to `sample_size = int(1.0 * len(data))`
- Train for more epochs: increase `NUM_EPOCHS` to 20-30
- Try different `LEARNING_RATE`: try 0.0001 or 0.0005

---

## Advanced: Using Full Dataset

To train on the complete dataset instead of 10%:

1. Edit `code/build_slot_dataset.py`, change line:
   ```python
   sample_size = int(1.0 * len(data))  # Use 100% instead of 0.1
   ```

2. Run:
   ```bash
   cd code
   python build_slot_dataset.py  # Takes 5-10 minutes
   python train.py               # Takes 1-2 hours on GPU
   ```

---

## Model Architecture

```
ResNet18 (Pre-trained on ImageNet)
    ↓
Feature Extraction (18 layers)
    ↓
Average Pooling
    ↓
Linear Layer (512 → 2 classes)
    ↓
Output: [Occupied, Vacant] Probabilities
```

- **Input:** 64×64 RGB images (normalized to [0, 1])
- **Output:** 2-class probabilities (Occupied / Vacant)
- **Training:** Cross-entropy loss + Adam optimizer
- **Parameters:** ~11.2 million (ResNet18)

---

## Performance Metrics

### On 10% Dataset (Current)
- **Training time:** ~3 min (GPU) / ~25 min (CPU)
- **Inference time:** ~0.1 sec/sample (GPU) / 1-2 sec/sample (CPU)
- **Model size:** 43 MB
- **Typical accuracy:** 80-90% on validation set

### On 100% Dataset (Optional)
- **Training time:** ~30-60 min (GPU) / ~4-6 hours (CPU)
- **Typical accuracy:** 85-95% on validation set

---

## Files Overview

### Code Directory Structure
```
code/
├── __init__.py              # Package initialization
├── train.py                 # Main training script (10 epochs)
├── build_slot_dataset.py    # Extract dataset (10% sample)
├── data_loader.py           # Load COCO annotations
├── preprocessor.py          # Crop and preprocess images
├── X_train.npy              # Training images (generated)
└── y_train.npy              # Training labels (generated)
```

### Key Imports
- `torch` - Deep learning framework
- `torchvision` - Pre-trained models (ResNet18)
- `numpy` - Array operations
- `cv2` - Image processing
- `json` - COCO annotation parsing

---

## Next Steps

1. **Train model:** `python code/build_slot_dataset.py && python code/train.py`
2. **Test model:** `python test_trained_model.py`
3. **Run web app:** `streamlit run app.py`
4. **Deploy:** Upload parking lot image → Get occupancy analysis

---

**Questions?** Check the module READMEs in each `moduleX_*/` directory.
