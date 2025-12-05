# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**Note:** First run will download YOLOv8 model (~6MB) automatically.

### Step 2: Test Camera

```bash
python test_camera.py
```

If camera doesn't work, try different camera index:
```bash
python test_camera.py 1
```

## Usage

### Method 1: Add Person Using Webcam

```bash
python add_person.py
```

- Enter person's name
- Position face in green box
- Press SPACE to capture
- Press ESC to cancel

### Method 2: Add Person Manually

1. Take a clear photo of the person's face
2. Save it in `database/persons/` folder
3. Name it: `person_name.jpg` (e.g., `john_doe.jpg`)

**Tips for best results:**
- Good lighting
- Face clearly visible
- Looking at camera
- No sunglasses or masks

### Run Detection System

```bash
python main.py
```

**Controls:**
- `q` - Quit
- `r` - Reload database (after adding new persons)
- `s` - Save screenshot
- `c` - Clear alert cooldowns

## How It Works

1. **YOLOv8** detects persons in camera feed
2. **Face Recognition** extracts and matches faces
3. **Alert System** triggers when known person is found
   - Visual alert banner (3 seconds)
   - Audio beep
   - Console log
   - Cooldown period (5 seconds)

## Configuration

Edit `config.py` to customize:

```python
# Camera
CAMERA_INDEX = 0  # Change if using external camera

# Detection
CONFIDENCE_THRESHOLD = 0.5  # Higher = fewer false positives

# Face Matching
FACE_MATCH_TOLERANCE = 0.6  # Lower = stricter matching

# Alerts
ALERT_COOLDOWN = 5  # Seconds between alerts
```

## Troubleshooting

### Camera not opening
- Check if another app is using the camera
- Try different `CAMERA_INDEX` (0, 1, 2...)
- Restart computer

### Poor face recognition
- Improve lighting
- Add multiple photos of same person
- Adjust `FACE_MATCH_TOLERANCE` (try 0.5 or 0.55)
- Ensure database photos are clear

### Slow performance
- Use smaller YOLOv8 model: `YOLO_MODEL = 'yolov8n.pt'`
- Reduce camera resolution in `config.py`
- Enable frame skipping: `SKIP_FRAMES = 1`

### No alerts
- Check if person is in database: `database/persons/`
- Press `r` to reload database
- Check console for face detection messages
- Verify face is visible in camera

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Camera:** Any USB/built-in webcam
- **OS:** Windows, Linux, or macOS

## Performance

- **YOLOv8n:** ~30 FPS (recommended)
- **YOLOv8s:** ~20 FPS
- **YOLOv8m:** ~10 FPS
- **YOLOv8l/x:** ~5 FPS (high accuracy)

*FPS varies by hardware*

## Example Workflow

```bash
# 1. Test camera
python test_camera.py

# 2. Add yourself to database
python add_person.py
# Enter name: "John Doe"
# Capture image

# 3. Add more people (optional)
# Copy photos to database/persons/jane_smith.jpg

# 4. Run detection
python main.py

# 5. When you appear on camera -> ALERT!
```

## Next Steps

- Add multiple photos per person for better accuracy
- Adjust configuration for your environment
- Integrate with other systems (webhook, email, etc.)
- Add logging to file
- Create web interface

## Support

For issues or questions:
1. Check `README.md` for detailed documentation
2. Review configuration in `config.py`
3. Check console output for error messages
