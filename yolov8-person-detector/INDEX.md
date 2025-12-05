# 📑 Project Index - YOLOv8 Person Detection System

Complete file reference and navigation guide.

---

## 🚀 START HERE

| File | Purpose | When to Use |
|------|---------|-------------|
| **GETTING_STARTED.md** | Step-by-step setup guide | First time setup |
| **QUICKSTART.md** | Quick reference | Fast setup |
| **README.md** | Full documentation | Detailed info |

---

## 📂 Project Structure

```
yolov8-person-detector/
│
├── 📖 Documentation
│   ├── GETTING_STARTED.md      ⭐ Start here for beginners
│   ├── QUICKSTART.md           ⚡ Quick setup guide
│   ├── README.md               📚 Full documentation
│   ├── PROJECT_SUMMARY.md      📊 Complete overview
│   └── INDEX.md                📑 This file
│
├── 🐍 Core Application
│   ├── main.py                 🎯 Main entry point - RUN THIS
│   ├── person_detector.py      👤 YOLOv8 person detection
│   ├── face_matcher.py         😊 Face recognition & matching
│   ├── alert_system.py         🚨 Alert notifications
│   └── config.py               ⚙️ Configuration settings
│
├── 🛠️ Utilities
│   ├── add_person.py           📸 Add person via webcam
│   ├── test_camera.py          🎥 Test camera functionality
│   ├── install.bat             💻 Windows installer
│   └── install.sh              🐧 Linux/Mac installer
│
├── 📁 Database
│   └── database/
│       ├── README.md           📖 Database usage guide
│       └── persons/            🗂️ Store person images here
│
├── 🔌 Integration Examples
│   └── examples/
│       ├── README.md           📖 Integration guide
│       ├── webhook_integration.py  🌐 HTTP webhook alerts
│       └── email_notification.py   📧 Email alerts
│
└── 📦 Configuration
    ├── requirements.txt        📋 Python dependencies
    └── .gitignore             🚫 Git ignore rules
```

---

## 🎯 Quick Navigation

### I want to...

#### 🆕 Get Started
→ Read **GETTING_STARTED.md**  
→ Run `install.bat` (Windows) or `install.sh` (Linux/Mac)  
→ Run `python test_camera.py`

#### 🏃 Run the System
→ Run `python main.py`  
→ See **QUICKSTART.md** for controls

#### 👤 Add People
→ Run `python add_person.py` (webcam)  
→ Or copy images to `database/persons/`  
→ See `database/README.md` for guidelines

#### ⚙️ Configure Settings
→ Edit `config.py`  
→ See **README.md** for all options

#### 🔧 Troubleshoot
→ Check **GETTING_STARTED.md** troubleshooting section  
→ Run `python test_camera.py` to test camera  
→ Check console output for errors

#### 🔌 Integrate with Other Systems
→ See `examples/README.md`  
→ Use `examples/webhook_integration.py`  
→ Use `examples/email_notification.py`

#### 📚 Learn More
→ Read **PROJECT_SUMMARY.md** for complete overview  
→ Read **README.md** for detailed documentation

---

## 📄 File Descriptions

### Documentation Files

**GETTING_STARTED.md** (8.5 KB)
- Complete beginner's guide
- Step-by-step instructions
- Troubleshooting tips
- FAQ section

**QUICKSTART.md** (3.4 KB)
- Fast setup instructions
- Quick reference
- Essential commands
- Common configurations

**README.md** (2.4 KB)
- Project overview
- Feature list
- Installation guide
- Usage instructions

**PROJECT_SUMMARY.md** (8.0 KB)
- Comprehensive overview
- Architecture details
- Use cases
- Future enhancements

**INDEX.md** (This file)
- File navigation
- Quick reference
- Project structure

### Core Application Files

**main.py** (6.4 KB)
- Application entry point
- Main detection loop
- User interface
- Keyboard controls
```bash
python main.py  # Run this to start
```

**person_detector.py** (3.8 KB)
- YOLOv8 integration
- Person detection logic
- Bounding box drawing
- Detection filtering

**face_matcher.py** (4.6 KB)
- Face recognition
- Database loading
- Face encoding
- Matching algorithm

**alert_system.py** (4.1 KB)
- Alert triggering
- Audio notifications
- Alert logging
- Cooldown management

**config.py** (1.0 KB)
- Configuration settings
- Camera settings
- Detection parameters
- Alert settings

### Utility Files

**add_person.py** (3.0 KB)
- Interactive person addition
- Webcam capture
- Image saving
```bash
python add_person.py
```

**test_camera.py** (1.7 KB)
- Camera testing
- Resolution check
- FPS verification
```bash
python test_camera.py
```

**install.bat** (1.1 KB)
- Windows installation script
- Virtual environment setup
- Dependency installation
```bash
install.bat  # Double-click or run in cmd
```

**install.sh** (1.1 KB)
- Linux/Mac installation script
- Virtual environment setup
- Dependency installation
```bash
chmod +x install.sh && ./install.sh
```

### Database Files

**database/README.md** (2.1 KB)
- Database usage guide
- Photo guidelines
- Naming conventions
- Best practices

**database/persons/** (folder)
- Store person images here
- Supported: .jpg, .jpeg, .png, .bmp
- Naming: `firstname_lastname.jpg`

### Integration Examples

**examples/README.md** (3.2 KB)
- Integration guide
- Setup instructions
- Security best practices
- Custom integration template

**examples/webhook_integration.py** (1.5 KB)
- HTTP webhook alerts
- External system integration
- Example Flask server

**examples/email_notification.py** (2.8 KB)
- Email alert system
- Image attachments
- SMTP configuration
- Gmail setup guide

### Configuration Files

**requirements.txt** (112 bytes)
- Python package dependencies
- Version specifications
```
ultralytics==8.0.196
opencv-python==4.8.1.78
numpy==1.24.3
face-recognition==1.3.0
Pillow==10.0.1
pygame==2.5.2
```

**.gitignore** (411 bytes)
- Git ignore rules
- Excludes cache files
- Excludes virtual environments

---

## 🎓 Learning Path

### Beginner (Day 1)
1. Read **GETTING_STARTED.md**
2. Run `install.bat` or `install.sh`
3. Run `python test_camera.py`
4. Run `python add_person.py`
5. Run `python main.py`

### Intermediate (Week 1)
1. Read **README.md**
2. Experiment with `config.py`
3. Add multiple people
4. Test different lighting
5. Read `examples/README.md`

### Advanced (Month 1)
1. Read **PROJECT_SUMMARY.md**
2. Implement webhook integration
3. Set up email notifications
4. Modify core modules
5. Create custom integrations

---

## 📊 File Size Summary

| Category | Files | Total Size |
|----------|-------|------------|
| Documentation | 5 | ~30 KB |
| Core Application | 5 | ~24 KB |
| Utilities | 4 | ~7 KB |
| Examples | 3 | ~7 KB |
| Configuration | 2 | ~0.5 KB |
| **Total** | **19** | **~68 KB** |

*Excluding database images and downloaded models*

---

## 🔍 Search Guide

### Find by Topic

**Installation**
- GETTING_STARTED.md → Installation section
- QUICKSTART.md → Installation
- install.bat / install.sh

**Configuration**
- config.py → All settings
- GETTING_STARTED.md → Basic Configuration
- README.md → Configuration section

**Troubleshooting**
- GETTING_STARTED.md → Troubleshooting section
- QUICKSTART.md → Troubleshooting
- test_camera.py → Camera issues

**Integration**
- examples/README.md → Integration guide
- examples/webhook_integration.py → Webhooks
- examples/email_notification.py → Email

**Database Management**
- database/README.md → Database guide
- add_person.py → Add persons
- face_matcher.py → Matching logic

---

## 🎯 Common Tasks

### Task: Add a New Person

1. **Method A (Webcam):**
   ```bash
   python add_person.py
   ```

2. **Method B (Existing Photo):**
   - Copy photo to `database/persons/`
   - Name: `john_doe.jpg`
   - Press `r` in running app

**Reference:** `database/README.md`

### Task: Change Camera

1. Edit `config.py`
2. Change `CAMERA_INDEX = 1` (try 0, 1, 2...)
3. Test with `python test_camera.py`

**Reference:** `GETTING_STARTED.md` → Troubleshooting

### Task: Adjust Sensitivity

1. Edit `config.py`
2. Change `CONFIDENCE_THRESHOLD` (detection)
3. Change `FACE_MATCH_TOLERANCE` (matching)

**Reference:** `README.md` → Configuration

### Task: Add Email Alerts

1. Read `examples/README.md`
2. Copy code from `examples/email_notification.py`
3. Configure SMTP settings
4. Integrate into `main.py`

**Reference:** `examples/email_notification.py`

---

## 📞 Support Resources

| Issue | Resource |
|-------|----------|
| Setup problems | GETTING_STARTED.md |
| Camera issues | test_camera.py |
| Configuration | config.py + README.md |
| Database | database/README.md |
| Integration | examples/README.md |
| General help | PROJECT_SUMMARY.md |

---

## ✅ Checklist

### First Time Setup
- [ ] Read GETTING_STARTED.md
- [ ] Run installation script
- [ ] Test camera
- [ ] Add yourself to database
- [ ] Run main application
- [ ] Verify alert works

### Regular Use
- [ ] Activate virtual environment
- [ ] Run `python main.py`
- [ ] Add new persons as needed
- [ ] Adjust config if needed

### Maintenance
- [ ] Backup database folder
- [ ] Update person photos
- [ ] Review alert logs
- [ ] Update dependencies

---

## 🎉 Quick Command Reference

```bash
# Installation
install.bat              # Windows
./install.sh            # Linux/Mac

# Activation
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

# Testing
python test_camera.py   # Test camera

# Usage
python add_person.py    # Add person
python main.py          # Run system

# In-app controls
q - Quit
r - Reload database
s - Screenshot
c - Clear cooldowns
```

---

**Last Updated:** October 2025  
**Version:** 1.0  
**Total Files:** 19  
**Total Size:** ~68 KB (excluding models and database images)

---

*Happy detecting! 🚀*
