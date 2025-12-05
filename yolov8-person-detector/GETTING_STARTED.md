# 🚀 Getting Started with YOLOv8 Person Detection System

Welcome! This guide will help you set up and run the person detection system in **under 10 minutes**.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ **Python 3.8 or higher** installed
- ✅ **Webcam** (built-in or USB)
- ✅ **4GB RAM** minimum (8GB recommended)
- ✅ **Internet connection** (for initial setup)

### Check Python Version

```bash
python --version
# Should show Python 3.8.x or higher
```

---

## ⚡ Quick Installation (3 Steps)

### Windows Users

1. **Double-click** `install.bat`
2. Wait for installation to complete
3. Done! ✅

### Linux/Mac Users

```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🎯 First Run (5 Steps)

### Step 1: Test Your Camera

```bash
python test_camera.py
```

**Expected result:** You should see yourself on camera  
**If it doesn't work:** Try `python test_camera.py 1` (different camera)

### Step 2: Add Yourself to Database

```bash
python add_person.py
```

**What to do:**
1. Enter your name when prompted
2. Position your face in the green box
3. Press **SPACE** to capture
4. Press **ESC** if you want to cancel

**Tips:**
- Face the camera directly
- Ensure good lighting
- Remove sunglasses/masks
- Stay still when capturing

### Step 3: Run the Detection System

```bash
python main.py
```

**What you'll see:**
- Live camera feed
- Your face detected with bounding box
- Alert when you're recognized!
- FPS and statistics

### Step 4: Test the Alert

Move in front of the camera. You should see:
- 🟢 **Green box** around you
- 🚨 **Red alert banner** at top
- 🔊 **Beep sound**
- 📝 **Console message**

### Step 5: Add More People (Optional)

**Option A: Using webcam**
```bash
python add_person.py
```

**Option B: Using existing photos**
1. Copy photo to `database/persons/`
2. Name it: `john_doe.jpg`
3. Press `r` in running app to reload

---

## 🎮 Controls

While the system is running:

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Reload database (after adding new persons) |
| `s` | Save screenshot |
| `c` | Clear alert cooldowns |

---

## ⚙️ Basic Configuration

Edit `config.py` to customize:

### Change Camera

```python
CAMERA_INDEX = 1  # Try 0, 1, 2... until you find your camera
```

### Adjust Detection Sensitivity

```python
CONFIDENCE_THRESHOLD = 0.5  # Higher = fewer false positives (0.0 - 1.0)
```

### Adjust Face Matching

```python
FACE_MATCH_TOLERANCE = 0.6  # Lower = stricter matching (0.4 - 0.7)
```

### Change Alert Frequency

```python
ALERT_COOLDOWN = 5  # Seconds between alerts for same person
```

---

## 🎨 Understanding the Display

### Bounding Box Colors

- 🟢 **Green** = Known person (matched with database)
- 🟠 **Orange** = Unknown person (not in database)

### Info Panel (Bottom Left)

```
FPS: 28.5                    # Frames per second
Persons detected: 2          # Number of people in frame
Database: 5 persons          # People in your database
Time: 14:30:45              # Current time
```

### Alert Banner (Top)

Appears for 3 seconds when known person is detected:
```
🚨 ALERT: John Doe DETECTED!
Confidence: 95.2%
```

---

## 📸 Photo Guidelines

For best recognition results:

### ✅ Good Photos

- Direct face-on angle
- Good lighting (natural light is best)
- Clear, sharp image
- Neutral expression
- No obstructions

### ❌ Bad Photos

- Dark or backlit
- Blurry or low quality
- Extreme angles
- Sunglasses or masks
- Group photos

### Example

```
Good:  😊 (front view, well-lit, clear)
Bad:   😎 (sunglasses, side view, dark)
```

---

## 🔧 Troubleshooting

### Camera Not Opening

**Problem:** "Error: Could not open camera"

**Solutions:**
1. Close other apps using camera (Zoom, Skype, etc.)
2. Try different camera index:
   ```python
   # In config.py
   CAMERA_INDEX = 1  # or 2, 3...
   ```
3. Restart computer
4. Check camera permissions

### No Face Detection

**Problem:** Person detected but not recognized

**Solutions:**
1. Improve lighting
2. Face camera directly
3. Check database has images:
   ```bash
   dir database\persons\  # Windows
   ls database/persons/   # Linux/Mac
   ```
4. Reload database (press `r`)

### False Matches

**Problem:** Wrong person identified

**Solutions:**
1. Lower tolerance (stricter):
   ```python
   FACE_MATCH_TOLERANCE = 0.5  # was 0.6
   ```
2. Use better quality photos
3. Add multiple angles of same person

### Slow Performance

**Problem:** Low FPS, laggy

**Solutions:**
1. Use faster model:
   ```python
   YOLO_MODEL = 'yolov8n.pt'  # Fastest
   ```
2. Reduce resolution:
   ```python
   CAMERA_WIDTH = 640
   CAMERA_HEIGHT = 480
   ```
3. Skip frames:
   ```python
   SKIP_FRAMES = 1  # Process every other frame
   ```

---

## 📚 Next Steps

### Beginner

1. ✅ Add family members to database
2. ✅ Experiment with different settings
3. ✅ Try different lighting conditions

### Intermediate

1. 📧 Set up email notifications (see `examples/`)
2. 🔗 Add webhook integration
3. 📊 Create alert logs

### Advanced

1. 🌐 Build web interface
2. 📹 Add video recording
3. 🔄 Multi-camera support
4. ☁️ Cloud integration

---

## 📖 Documentation

- **QUICKSTART.md** - Quick reference guide
- **README.md** - Full documentation
- **PROJECT_SUMMARY.md** - Complete overview
- **examples/README.md** - Integration examples

---

## 💡 Tips & Tricks

### Tip 1: Multiple Photos Per Person

For better accuracy, add photos in different conditions:
```
database/persons/
  ├── john_morning.jpg      # Morning light
  ├── john_evening.jpg      # Evening light
  └── john_glasses.jpg      # With glasses
```

### Tip 2: Organize Your Database

Use clear naming:
```
john_doe.jpg          ✅ Good
jane_smith.jpg        ✅ Good
IMG_1234.jpg          ❌ Bad
person.jpg            ❌ Bad
```

### Tip 3: Test Different Times

Face recognition can vary with lighting. Test:
- Morning (natural light)
- Afternoon (bright)
- Evening (artificial light)
- Night (low light)

### Tip 4: Backup Your Database

```bash
# Windows
xcopy database\persons database_backup\persons /E /I

# Linux/Mac
cp -r database/persons database_backup/persons
```

---

## 🎯 Common Use Cases

### Home Security

```python
# config.py
ALERT_COOLDOWN = 10  # Less frequent alerts
CONFIDENCE_THRESHOLD = 0.6  # Higher confidence
```

### Office Attendance

```python
# config.py
ALERT_COOLDOWN = 300  # Once per person per 5 min
FACE_MATCH_TOLERANCE = 0.5  # Strict matching
```

### Visitor Recognition

```python
# config.py
ALERT_COOLDOWN = 3  # Frequent alerts
FACE_MATCH_TOLERANCE = 0.6  # Balanced
```

---

## ❓ FAQ

**Q: How many people can I add to the database?**  
A: Unlimited, but performance may decrease with 100+ people.

**Q: Can it detect multiple people at once?**  
A: Yes! It detects all persons in frame simultaneously.

**Q: Does it work in the dark?**  
A: Face recognition needs visible faces. Use good lighting.

**Q: Can I use a video file instead of camera?**  
A: Yes, modify `main.py` to use `cv2.VideoCapture('video.mp4')`.

**Q: Is internet required after installation?**  
A: No, runs completely offline.

**Q: How accurate is it?**  
A: 90-95% with good photos and lighting.

---

## 🆘 Getting Help

If you're stuck:

1. Check **Troubleshooting** section above
2. Review error messages in console
3. Test camera with `test_camera.py`
4. Verify database has images
5. Check configuration in `config.py`

---

## 🎉 You're Ready!

You now have a working person detection system!

**Quick command reference:**
```bash
python test_camera.py    # Test camera
python add_person.py     # Add person
python main.py           # Run system
```

**Happy detecting! 🚀**

---

*Last updated: October 2025*
