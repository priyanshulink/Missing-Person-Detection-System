# 🎯 YOLOv8 Person Detection and Recognition System

A complete real-time person detection and recognition system using **YOLOv8** for person detection and **face recognition** for matching against a database of known persons.

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- ✅ **Real-time Person Detection** using YOLOv8
- ✅ **Face Recognition** and matching against database
- ✅ **Multi-person Detection** - detects multiple people simultaneously
- ✅ **Alert System** with visual banners and audio notifications
- ✅ **Database Management** for known persons
- ✅ **Live Camera Feed** with annotated bounding boxes
- ✅ **Performance Metrics** - FPS counter and statistics
- ✅ **Easy Configuration** - no code changes needed
- ✅ **Integration Examples** - webhooks, email notifications

---

## 🚀 Quick Start

### 1️⃣ Installation (One Command)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh && ./install.sh
```

### 2️⃣ Add Yourself to Database

```bash
python add_person.py
```

### 3️⃣ Run Detection System

```bash
python main.py
```

**That's it! 🎉**

For detailed instructions, see **[GETTING_STARTED.md](GETTING_STARTED.md)**

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Complete beginner's guide with step-by-step instructions |
| **[QUICKSTART.md](QUICKSTART.md)** | Quick reference for fast setup |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Comprehensive project overview |
| **[INDEX.md](INDEX.md)** | File navigation and quick reference |
| **[database/README.md](database/README.md)** | Database usage and photo guidelines |
| **[examples/README.md](examples/README.md)** | Integration examples (webhooks, email) |

---

## 🎮 Controls

While running `main.py`:

| Key | Action |
|-----|--------|
| `q` | Quit application |
| `r` | Reload database (after adding new persons) |
| `s` | Save screenshot |
| `c` | Clear alert cooldowns |

---

## 📁 Project Structure

```
yolov8-person-detector/
│
├── 📖 Documentation
│   ├── GETTING_STARTED.md      ⭐ Start here!
│   ├── QUICKSTART.md
│   ├── PROJECT_SUMMARY.md
│   └── INDEX.md
│
├── 🐍 Core Application
│   ├── main.py                 🎯 Run this
│   ├── person_detector.py
│   ├── face_matcher.py
│   ├── alert_system.py
│   └── config.py               ⚙️ Edit settings here
│
├── 🛠️ Utilities
│   ├── add_person.py           📸 Add persons
│   ├── test_camera.py          🎥 Test camera
│   ├── install.bat
│   └── install.sh
│
├── 📁 Database
│   └── database/persons/       🗂️ Store images here
│
└── 🔌 Examples
    └── examples/
        ├── webhook_integration.py
        └── email_notification.py
```

---

## ⚙️ Configuration

Edit **`config.py`** to customize:

```python
# Camera Settings
CAMERA_INDEX = 0              # Change camera (0, 1, 2...)
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Detection Settings
YOLO_MODEL = 'yolov8n.pt'     # Model: n, s, m, l, x
CONFIDENCE_THRESHOLD = 0.5     # Detection confidence

# Face Recognition
FACE_MATCH_TOLERANCE = 0.6     # Lower = stricter (0.4-0.7)

# Alerts
ALERT_COOLDOWN = 5             # Seconds between alerts
```

---

## 🎯 How It Works

```
Camera Feed → YOLOv8 Detection → Face Extraction → Face Matching → Alert!
```

1. **YOLOv8** detects all persons in camera feed
2. **Face Recognition** extracts faces from detected persons
3. **Matching** compares faces against database
4. **Alert** triggers when known person is found

---

## 📦 Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Camera:** Any USB or built-in webcam
- **OS:** Windows, Linux, or macOS

### Dependencies

```
ultralytics==8.0.196      # YOLOv8
opencv-python==4.8.1.78   # Computer vision
face-recognition==1.3.0   # Face recognition
numpy==1.24.3             # Numerical computing
Pillow==10.0.1            # Image processing
pygame==2.5.2             # Audio alerts
```

---

## 🎨 Screenshots & Display

### Bounding Box Colors
- 🟢 **Green** = Known person (matched)
- 🟠 **Orange** = Unknown person

### Alert Banner
When a known person is detected:
```
🚨 ALERT: John Doe DETECTED!
Confidence: 95.2%
```

### Info Panel
```
FPS: 28.5
Persons detected: 2
Database: 5 persons
Time: 14:30:45
```

---

## 🔧 Troubleshooting

### Camera Not Opening
```bash
# Test camera
python test_camera.py

# Try different camera index
python test_camera.py 1
```

### Poor Recognition
- Improve lighting
- Use better quality photos
- Adjust `FACE_MATCH_TOLERANCE` in `config.py`

### Slow Performance
- Use faster model: `YOLO_MODEL = 'yolov8n.pt'`
- Reduce resolution in `config.py`

**For detailed troubleshooting, see [GETTING_STARTED.md](GETTING_STARTED.md)**

---

## 🔌 Integration Examples

### Webhook Alerts
```python
from examples.webhook_integration import WebhookAlert

webhook = WebhookAlert("https://your-server.com/api/alerts")
webhook.send_alert(person_name, confidence)
```

### Email Notifications
```python
from examples.email_notification import EmailAlert

email = EmailAlert(smtp_server, port, email, password)
email.send_alert(person_name, confidence, recipient, frame)
```

**See [examples/README.md](examples/README.md) for more**

---

## 📸 Database Guidelines

### Adding Persons

**Method 1: Webcam (Recommended)**
```bash
python add_person.py
```

**Method 2: Manual**
1. Copy photo to `database/persons/`
2. Name: `firstname_lastname.jpg`
3. Press `r` in app to reload

### Photo Tips

✅ **Good:**
- Front-facing angle
- Good lighting
- Clear, sharp image
- Neutral expression

❌ **Bad:**
- Dark or blurry
- Sunglasses/masks
- Extreme angles
- Group photos

---

## 🎯 Use Cases

- 🏠 **Home Security** - Detect family vs strangers
- 🏢 **Office Access** - Monitor authorized personnel
- 🛍️ **Retail** - Identify VIP customers
- 🎫 **Events** - Track registered attendees
- 🚪 **Smart Doorbell** - Recognize visitors
- ✅ **Attendance** - Automated check-in

---

## 📊 Performance

| Model | FPS | Accuracy | Best For |
|-------|-----|----------|----------|
| yolov8n | ~30 | Good | Real-time |
| yolov8s | ~20 | Better | Balanced |
| yolov8m | ~10 | High | Accuracy |
| yolov8l | ~5 | Very High | Maximum accuracy |

*Performance varies by hardware*

---

## 🚀 Next Steps

### Beginner
1. Add family members to database
2. Experiment with settings
3. Test different lighting

### Advanced
1. Set up email notifications
2. Add webhook integration
3. Build web interface
4. Multi-camera support

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## 🙏 Acknowledgments

Built with:
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [OpenCV](https://opencv.org/)
- [PyGame](https://www.pygame.org/)

---

## 📞 Support

- 📖 Read [GETTING_STARTED.md](GETTING_STARTED.md) for detailed help
- 🔍 Check [INDEX.md](INDEX.md) for file navigation
- 💡 See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for overview

---

**Version:** 1.0  
**Status:** Production Ready ✅  
**Last Updated:** October 2025

---

**Ready to get started? → [GETTING_STARTED.md](GETTING_STARTED.md)** 🚀
