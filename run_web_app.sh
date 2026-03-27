#!/bin/bash
# Parking Space Detection Web App Launcher
# macOS/Linux shell script to easily run the Streamlit app

echo ""
echo "========================================"
echo "  Parking Space Detection Web App"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -m pip show streamlit &> /dev/null; then
    echo "Installing Streamlit..."
    python3 -m pip install streamlit
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Streamlit"
        exit 1
    fi
fi

# Check if model exists
if [ ! -f "module4_deep_learning/resnet18_parking.pth" ]; then
    echo ""
    echo "Error: Trained model not found at:"
    echo "  module4_deep_learning/resnet18_parking.pth"
    echo ""
    echo "Please ensure the model file exists and try again."
    exit 1
fi

echo ""
echo "Starting Parking Space Detection Web App..."
echo ""
echo "✓ Opening browser at: http://localhost:8501"
echo "✓ Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

# Run Streamlit app
python3 -m streamlit run app.py --logger.level=warning
