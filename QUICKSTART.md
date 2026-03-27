# 🚀 Web App Quick Start Guide

## What You Just Got

A professional web interface for your parking space detection model with:
- 📸 Image upload capability
- 🤖 Real-time AI predictions  
- 📊 Confidence scores & visual results
- 🎛️ Configurable inference parameters

---

## ⚡ Start the Web App (Choose One)

### Option 1: Windows Users (Easiest)
**Double-click** this file in your project folder:
```
run_web_app.bat
```
Your browser will automatically open to the app!

### Option 2: Mac/Linux Users
Open terminal and run:
```bash
cd "/path/to/ParkingSpaceDetectionMP"
bash run_web_app.sh
```

### Option 3: Manual (All Platforms)
```bash
cd "C:\Users\KIIT0001\Desktop\PYTHON PROJECTS\MINI-P\ParkingSpaceDetectionMP"
streamlit run app.py
```

---

## 🎮 Using the Web App

### Step 1️⃣: Load the Model
1. Open the app (browser shows at `http://localhost:8501`)
2. Look at the **LEFT SIDEBAR** ⬅️
3. You'll see:
   - 📱 Processing Device selector
   - 🎛️ Confidence Threshold slider
   - 🔄 "Load Model" button

4. Click the **"Load Model"** button
5. Wait for ✅ **Model Ready** message
   - First load may take 10-15 seconds
   - Subsequent loads are instant (cached)

### Step 2️⃣: Upload Image
1. In the **main area**, click the upload box
2. **Drag & drop** a parking lot image OR click to browse
3. Image preview appears immediately

### Step 3️⃣: Analyze
1. Click the **"🔍 Analyze Image"** button
2. Wait ~1 second for inference
3. See results in the **RIGHT PANEL** 📊

### Step 4️⃣: View Results
You'll see:
- 🔴 **OCCUPIED** (Red) - Space has a car
- 🟢 **VACANT** (Green) - Space is empty
- **Confidence %** - How sure the model is (higher = better)
- **Status badge** - Large color-coded indicator

---

## 📸 Example Workflow

```
1. Open browser → http://localhost:8501

2. [SIDEBAR] Select Device: "CPU" or "GPU"

3. [SIDEBAR] Adjust Threshold: 0.5 (50%)

4. [SIDEBAR] Click "Load Model"
   ↓
   [Wait] ✅ Model loaded!

5. [MAIN AREA] Upload parking lot image
   ↓
   [Shows preview]

6. [MAIN AREA] Click "Analyze Image"
   ↓
   [RIGHT PANEL] Shows result:
   - Status: 🟢 VACANT
   - Confidence: 92.3%
   - Details displayed
```

---

## ⚙️ Configuration Options

### Processing Device
- **CPU** (Default)
  - ✅ Works on any computer
  - ✅ ~100ms inference time
  - ✅ No NVIDIA GPU required
  
- **GPU (CUDA)**
  - ✅ Much faster (~20ms)
  - ❌ Requires NVIDIA GPU
  - ❌ Requires CUDA 11.8+
  - ⚠️ Only available if CUDA is installed

### Confidence Threshold
- **Lower (0.3-0.4)**: More aggressive detection
- **Default (0.5)**: Balanced
- **Higher (0.7-0.8)**: Conservative detection

**How it works:**
- Model outputs occupancy probability (0-100%)
- If probability ≥ threshold → **OCCUPIED**
- If probability < threshold → **VACANT**

---

## 📱 Testing the App

### Test Image 1: Occupied Space
Expected: Status "OCCUPIED", High confidence
```bash
# Use any image with parked cars
# Try: datasets/test/2012-09-11_15_53_00_jpg.rf.8282544a640a23df05bd245a9210e663.jpg
```

### Test Image 2: Empty Space  
Expected: Status "VACANT", Lower confidence
```bash
# Use images with empty spaces
# Try: datasets/test/2012-09-12_14_12_08_jpg.rf.667489b9945bf933e519cc5c39c3a084.jpg
```

---

## 🌐 Advanced: Access from Other Devices

Want to use the app on your phone or another computer?

### On Same WiFi Network:

**Step 1: Find your computer's IP**
- Windows: Open Command Prompt, type `ipconfig`
- Look for IPv4 Address (e.g., `192.168.1.100`)

**Step 2: Run app with network access**
```bash
streamlit run app.py --server.address 0.0.0.0
```

**Step 3: Open on another device**
Open browser and go to:
```
http://YOUR_COMPUTER_IP:8501
```
Example: `http://192.168.1.100:8501`

---

## 📊 Understanding Results

### Confidence Score
A score from 0% (definitely vacant) to 100% (definitely occupied)

```
0%                50%               100%
|--VACANT---------|--OCCUPIED--------|
|                 |                 |
Clear empty space Uncertain zone    Car present
```

### Performance Notes
- **High Confidence (80-100%)**: Very reliable
- **Medium Confidence (50-80%)**: Generally accurate
- **Low Confidence (0-50%)**: May have errors

---

## 🎯 Best Practices

### ✅ DO
- Use clear, well-lit images
- Capture parking space from front or overhead
- Upload JPG or PNG format
- Use images similar to training data (PKLot dataset)
- Allow model to fully load before uploading

### ❌ DON'T
- Upload very small or blurry images
- Use extreme camera angles
- Submit images with multiple spaces at once
- Change device while model is running
- Close app during inference

---

## 🐛 Troubleshooting

### "Model failed to load"
```
✓ Check that resnet18_parking.pth exists (43MB file)
✓ Verify you're in the correct directory
✓ Run: cd "C:\...\ParkingSpaceDetectionMP"
✓ Then: streamlit run app.py
```

### "No such file or directory"
```
✓ Make sure you're in the project root directory
✓ File run_web_app.bat should be clickable from project folder
✓ If using manual method, double-check path
```

### "ModuleNotFoundError: No module named 'streamlit'"
```
# Install Streamlit
pip install streamlit

# Or run the launcher again - it will auto-install
```

### App is very slow
```
✓ Switch from GPU to CPU in sidebar
✓ Check available RAM and close other apps
✓ Refresh browser page (Ctrl+R or Cmd+R)
```

### Browser won't open
```
# Manual open:
# 1. Start the app from terminal
# 2. Manually go to: http://localhost:8501
```

---

## 📚 File Structure

```
ParkingSpaceDetectionMP/
├── app.py                    ← Web app (main file)
├── run_web_app.bat          ← Windows launcher (click me!)
├── run_web_app.sh           ← Mac/Linux launcher
├── WEB_APP_README.md        ← Detailed documentation
├── QUICKSTART.md            ← This file
│
├── module4_deep_learning/
│   └── resnet18_parking.pth ← Trained model (43MB)
│
└── datasets/
    └── test/                ← Test images for practice
```

---

## 💡 Next Steps

1. **Test the app** with provided test images
2. **Try with your own** parking lot photos
3. **Adjust settings** to see how they affect results
4. **Share with team** by accessing on other devices
5. **Deploy online** (optional - see WEB_APP_README.md)

---

## 📞 Support Resources

| Issue | Solution |
|-------|----------|
| Model not found | Run from correct directory |
| Streamlit not installed | `pip install streamlit` |
| Image won't upload | Check format (JPG/PNG only) |
| Slow inference | Use CPU, close other apps |
| App won't start | Check Python version (3.8+) |

---

## 🎓 Learning Resources

**Want to understand how it works?**
- Check [WEB_APP_README.md](WEB_APP_README.md) for detailed docs
- See [main.py](main.py) - full pipeline implementation
- Look at [code/train.py](code/train.py) - model training
- Review [README.md](README.md) - project overview

---

## ✅ Checklist

Before using the app:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Streamlit installed (`pip install streamlit`)
- [ ] In correct project directory
- [ ] Model file exists (43MB)
- [ ] Browser can access localhost

---

**Ready? Let's go! Click run_web_app.bat (Windows) or run run_web_app.sh (Mac/Linux) 🚀**

---

*Created: March 2026*  
*Parking Space Detection System v1.0*  
*Model: ResNet18 • Framework: PyTorch • UI: Streamlit*
