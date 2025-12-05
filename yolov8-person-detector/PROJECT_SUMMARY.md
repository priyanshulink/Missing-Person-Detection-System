# YOLOv8 Person Detection & Recognition System
## Project Summary

---

## 📁 Project Structure

```
yolov8-person-detector/
├── 📄 main.py                    # Main application entry point
├── 📄 person_detector.py         # YOLOv8 person detection module
├── 📄 face_matcher.py            # Face recognition & matching module
├── 📄 alert_system.py            # Alert notification system
├── 📄 config.py                  # Configuration settings
├── 📄 add_person.py              # Utility to add persons via webcam
├── 📄 test_camera.py             # Camera testing utility
├── 📄 requirements.txt           # Python dependencies
├── 📄 install.bat / install.sh   # Installation scripts
├── 📄 README.md                  # Full documentation
├── 📄 QUICKSTART.md              # Quick start guide
├── 📄 .gitignore                 # Git ignore rules
└── 📁 database/
    ├── 📄 README.md              # Database usage guide
    └── 📁 persons/               # Store person images here
        └── .gitkeep
```

---

## 🎯 Features

### Core Functionality
- ✅ **Real-time Person Detection** using YOLOv8
- ✅ **Face Recognition** and matching against database
- ✅ **Alert System** with visual and audio notifications
- ✅ **Database Management** for known persons
- ✅ **Live Camera Feed** with annotations

### User Interface
- 📊 FPS counter and performance metrics
- 🎨 Color-coded bounding boxes (green = matched, orange = unknown)
- 🚨 Alert banners when known person detected
- ℹ️ Real-time info panel with statistics

### Controls
- `q` - Quit application
- `r` - Reload database
- `s` - Save screenshot
- `c` - Clear alert cooldowns

---

## 🚀 Quick Start

### 1. Installation (Windows)
```bash
install.bat
```

### 2. Installation (Linux/Mac)
```bash
chmod +x install.sh
./install.sh
```

### 3. Manual Installation
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 4. Add Person to Database
```bash
python add_person.py
```

### 5. Run Detection System
```bash
python main.py
```

---

## 🔧 Configuration

Edit `config.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `CAMERA_INDEX` | 0 | Camera device index |
| `YOLO_MODEL` | yolov8n.pt | YOLOv8 model variant |
| `CONFIDENCE_THRESHOLD` | 0.5 | Person detection confidence |
| `FACE_MATCH_TOLERANCE` | 0.6 | Face matching strictness |
| `ALERT_COOLDOWN` | 5 | Seconds between alerts |

---

## 📦 Dependencies

```
ultralytics==8.0.196      # YOLOv8 for person detection
opencv-python==4.8.1.78   # Computer vision library
numpy==1.24.3             # Numerical computing
face-recognition==1.3.0   # Face recognition library
Pillow==10.0.1            # Image processing
pygame==2.5.2             # Audio alerts
```

---

## 🎬 How It Works

```
┌─────────────┐
│ Camera Feed │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ YOLOv8 Detector │ ──► Detect all persons in frame
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ Face Extraction  │ ──► Extract faces from detected persons
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Face Matching   │ ──► Compare with database
└────────┬─────────┘
         │
         ▼
    Match Found?
         │
    ┌────┴────┐
    │   YES   │
    └────┬────┘
         │
         ▼
┌──────────────────┐
│  Alert System    │ ──► Visual + Audio + Log
└──────────────────┘
```

---

## 🎯 Use Cases

1. **Home Security** - Detect family members vs strangers
2. **Office Access** - Monitor authorized personnel
3. **Retail** - Identify VIP customers
4. **Event Management** - Track registered attendees
5. **Smart Doorbell** - Recognize visitors
6. **Attendance System** - Automated check-in

---

## 📊 Performance

| Model | Speed (FPS) | Accuracy | Use Case |
|-------|-------------|----------|----------|
| YOLOv8n | ~30 | Good | Real-time, standard |
| YOLOv8s | ~20 | Better | Balanced |
| YOLOv8m | ~10 | High | Accuracy priority |
| YOLOv8l | ~5 | Very High | Maximum accuracy |

*Performance varies by hardware*

---

## 🔍 Troubleshooting

### Camera Issues
- **Not opening**: Check if another app is using it
- **Wrong camera**: Change `CAMERA_INDEX` in config.py
- **Poor quality**: Adjust resolution in config.py

### Recognition Issues
- **No matches**: Check database has images
- **False matches**: Lower `FACE_MATCH_TOLERANCE` (try 0.5)
- **Missed matches**: Increase `FACE_MATCH_TOLERANCE` (try 0.65)
- **Poor lighting**: Improve environment lighting

### Performance Issues
- **Slow FPS**: Use yolov8n.pt model
- **High CPU**: Enable frame skipping
- **Memory issues**: Reduce camera resolution

---

## 🔐 Security & Privacy

⚠️ **Important Considerations:**
- Only add photos with proper consent
- Secure the `database/persons/` folder
- Consider data protection regulations (GDPR, etc.)
- Use encryption for sensitive deployments
- Implement access controls
- Regular security audits

---

## 🚀 Future Enhancements

Potential improvements:
- [ ] Web interface for remote monitoring
- [ ] Email/SMS notifications
- [ ] Database with SQLite/PostgreSQL
- [ ] Multiple camera support
- [ ] Cloud integration
- [ ] Mobile app
- [ ] Video recording on alert
- [ ] Analytics dashboard
- [ ] API endpoints
- [ ] Docker containerization

---

## 📝 File Descriptions

### Core Modules

**main.py**
- Application entry point
- Integrates all modules
- Handles user input and display

**person_detector.py**
- YOLOv8 integration
- Person detection logic
- Bounding box drawing

**face_matcher.py**
- Face recognition using face_recognition library
- Database loading and management
- Face encoding and matching

**alert_system.py**
- Alert triggering logic
- Audio notifications (pygame)
- Alert logging and cooldown management

### Utilities

**add_person.py**
- Interactive person addition
- Webcam capture interface
- Database file management

**test_camera.py**
- Camera functionality testing
- Resolution and FPS checking
- Quick diagnostics

**config.py**
- Centralized configuration
- Easy parameter tuning
- No code changes needed

---

## 💡 Tips for Best Results

### Photo Quality
1. Use good lighting (natural light preferred)
2. Face should fill 30-50% of frame
3. Direct face-on angle
4. Neutral expression
5. No obstructions (glasses OK, sunglasses not OK)

### System Setup
1. Position camera at eye level
2. Ensure good ambient lighting
3. Minimize background movement
4. Stable camera mount
5. Test different times of day

### Database Management
1. One clear photo per person
2. Update photos if appearance changes significantly
3. Remove outdated entries
4. Organize with clear naming
5. Backup database regularly

---

## 📞 Support

For issues:
1. Check `QUICKSTART.md` for common solutions
2. Review `README.md` for detailed docs
3. Check console output for errors
4. Verify configuration in `config.py`
5. Test camera with `test_camera.py`

---

## 📄 License

This project is provided as-is for educational and personal use.

---

## 🙏 Acknowledgments

Built with:
- **Ultralytics YOLOv8** - Object detection
- **face_recognition** - Face recognition
- **OpenCV** - Computer vision
- **PyGame** - Audio alerts

---

**Created:** October 2025  
**Version:** 1.0  
**Status:** Production Ready ✅
