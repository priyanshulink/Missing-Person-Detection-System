#!/bin/bash

echo "============================================================"
echo "YOLOv8 Person Detection System - Installation"
echo "============================================================"
echo ""

echo "[1/3] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "Make sure Python 3.8+ is installed"
    exit 1
fi

echo "[2/3] Activating virtual environment..."
source venv/bin/activate

echo "[3/3] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "============================================================"
echo "Installation Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Run: source venv/bin/activate"
echo "  2. Test camera: python test_camera.py"
echo "  3. Add person: python add_person.py"
echo "  4. Run system: python main.py"
echo ""
echo "See QUICKSTART.md for detailed instructions"
echo ""
