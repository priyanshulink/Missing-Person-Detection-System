# System Startup Guide

## Quick Start

### Start Everything (Including All Cameras)
```bash
.\start_all.bat
```

This will automatically start:
1. ✅ MongoDB Database
2. ✅ Backend API Server (http://localhost:3000)
3. ✅ Frontend Dashboard (http://localhost:8080)
4. ✅ Multi-Camera Surveillance System
5. ✅ All active cameras start streaming

### Stop Everything
```bash
.\stop_all.bat
```

This will stop:
1. ❌ Multi-Camera Surveillance
2. ❌ Backend API
3. ❌ Frontend
4. ❌ All camera streams
5. ❌ All Python/Node processes

## What Happens When You Start

### Step-by-Step Process

**1. MongoDB Check**
```
[1/4] Checking MongoDB...
      MongoDB is running
```

**2. Backend API Starts**
```
[2/4] Starting Backend API Server...
      Backend API started on http://localhost:3000
```
- Opens new window: "Backend API"
- Connects to MongoDB
- Loads camera configurations
- Ready to receive detections

**3. Frontend Starts**
```
[3/4] Starting Frontend Server...
      Frontend started on http://localhost:8080
```
- Opens new window: "Frontend"
- Serves dashboard
- Ready for login

**4. Backend Ready**
```
[4/5] Waiting for backend to be ready...
```
- Waits 3 seconds for backend initialization

**5. Multi-Camera Surveillance Starts**
```
[5/5] Starting Multi-Camera Surveillance System...
      Multi-Camera Surveillance started
```
- Opens new window: "Multi-Camera Surveillance"
- Loads active cameras from database
- Creates thread for each camera
- Starts YOLO detection
- Begins face matching

### Active Cameras

When system starts, these cameras begin streaming:

**Library Hall Camera (cam02)**
- URL: http://10.28.71.10:8080/video
- Location: Library First Floor
- Status: Active

**Local Webcam (cam_local)**
- URL: 0 (default webcam)
- Location: Development Machine
- Status: Active

## System Windows

After running `start_all.bat`, you'll see 4 windows:

1. **Startup Script** - Shows startup progress
2. **Backend API** - Node.js server logs
3. **Frontend** - Python HTTP server
4. **Multi-Camera Surveillance** - Camera processing logs

## Multi-Camera Surveillance Window

You'll see output like:
```
============================================================
Multi-Camera Surveillance System
============================================================
🔄 Loading YOLOv8 model...
✅ YOLOv8 model loaded
🔄 Loading camera configurations...
✅ Loaded 2 active cameras

🚀 Starting surveillance on 2 cameras...

📹 Initialized camera: Library Hall Camera (cam02)
📹 Initialized camera: Local Webcam (cam_local)

✅ All cameras started

[Library Hall Camera] 🎥 Starting stream processing...
[Library Hall Camera] ✅ Loaded 15 face encodings
[Local Webcam] 🎥 Starting stream processing...
[Local Webcam] ✅ Loaded 15 face encodings

Press Ctrl+C to stop
```

## When Person is Detected

### Console Output
```
[Library Hall Camera] 🚨 ALERT: John Doe detected (similarity: 87.5%)
```

### Dashboard Alert
- Real-time notification appears
- Shows person name
- Shows camera name and location
- Shows detection time
- Provides "Confirm" button

### Database
- Report created automatically
- Links to person
- Links to camera
- Includes timestamp and similarity

## Controlling Individual Cameras

### While System is Running

**Check camera status:**
```bash
camera_control.bat status cam02
```

**Stop specific camera:**
```bash
camera_control.bat stop cam02
```

**Start specific camera:**
```bash
camera_control.bat start cam02
```

**Note:** Changes take effect within 30 seconds (next database refresh)

## Accessing the System

### Dashboard
```
URL: http://localhost:8080
Username: ompriyanshu12@gmail.com
Password: pradeep3133
```

### API
```
URL: http://localhost:3000
Endpoints:
  - GET  /api/cameras
  - GET  /api/persons
  - GET  /api/reports
  - POST /api/recognize
```

## Monitoring

### Check if Everything is Running

**Backend API:**
```bash
curl http://localhost:3000/health
```

**Frontend:**
```bash
curl http://localhost:8080
```

**Cameras:**
```bash
camera_control.bat list
```

### View Logs

**Backend Logs:**
- Check "Backend API" window

**Surveillance Logs:**
- Check "Multi-Camera Surveillance" window

**Camera Status:**
```bash
GET http://localhost:3000/api/cameras
```

## Troubleshooting

### System Won't Start

**MongoDB Not Running:**
```bash
net start MongoDB
```

**Port Already in Use:**
- Close other applications using ports 3000 or 8080
- Or change ports in configuration

**Python Not Found:**
- Ensure Python is installed
- Add Python to PATH

### Cameras Not Streaming

**Check Camera Status:**
```bash
camera_control.bat list
```

**Test Camera Connection:**
```bash
python test_camera_stream.py
```

**Verify Camera is Active:**
```bash
camera_control.bat status cam02
```

**Restart Surveillance:**
1. Stop: `.\stop_all.bat`
2. Start: `.\start_all.bat`

### No Detections

**Check Person Database:**
- Ensure persons are added
- Verify face encodings exist
- Check face images are clear

**Check YOLO Model:**
- Verify yolov8n.pt exists
- Check model loads successfully

**Check Confidence Threshold:**
- Default: 0.5 for YOLO
- Default: 0.6 for face matching

## Performance Tips

### For Better Performance

**Reduce Frame Processing:**
Edit `multi_camera_surveillance.py`:
```python
PROCESS_EVERY_N_FRAMES = 3  # Process every 3rd frame
```

**Use Faster YOLO Model:**
```python
YOLO_MODEL_PATH = 'yolov8n.pt'  # Fastest
```

**Limit Cameras:**
- Stop unused cameras
- Use `camera_control.bat stop <camera_id>`

### For Better Accuracy

**Process More Frames:**
```python
PROCESS_EVERY_N_FRAMES = 1  # Process every frame
```

**Use Better YOLO Model:**
```python
YOLO_MODEL_PATH = 'yolov8s.pt'  # More accurate
```

**Adjust Thresholds:**
```python
YOLO_CONFIDENCE = 0.6
FACE_CONFIDENCE_THRESHOLD = 0.5
```

## Adding More Cameras

### Method 1: Seed Script
Edit `backend-api/seed-cameras.js` and add:
```javascript
{
  cameraId: 'cam05',
  name: 'New Camera',
  location: 'New Location',
  streamUrl: 'http://192.168.1.100:8080/video',
  status: 'active'
}
```

Then run:
```bash
cd backend-api
node seed-cameras.js
```

### Method 2: API
```bash
camera_control.bat list  # Shows current cameras
# Then use API to add new camera
```

### Method 3: Dashboard
- Add camera management UI to frontend
- Create/edit cameras through web interface

## Restart After Changes

After adding cameras or changing configurations:
```bash
.\stop_all.bat
.\start_all.bat
```

## Summary

**To start everything including all cameras:**
```bash
.\start_all.bat
```

**To stop everything:**
```bash
.\stop_all.bat
```

**To control individual cameras:**
```bash
camera_control.bat start cam02   # Start
camera_control.bat stop cam02    # Stop
camera_control.bat status cam02  # Check
```

That's it! The system is fully automated. 🚀
