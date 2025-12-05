# Quick Start: Multi-Camera System

## What Was Implemented

✅ **Camera Model** - MongoDB schema for camera configurations
✅ **Camera API Routes** - CRUD operations for camera management
✅ **Multi-Camera Processor** - Python script with threading support
✅ **Report Linking** - Reports now reference cameras
✅ **Frontend Updates** - Dashboard shows camera name and location
✅ **Seeding Script** - Easy camera setup

## Quick Setup (5 Minutes)

### Step 1: Seed Sample Cameras
```bash
cd backend-api
node seed-cameras.js
```

This creates 5 sample cameras including a local webcam.

### Step 2: Start Backend
```bash
cd backend-api
npm start
```

### Step 3: Start Multi-Camera Surveillance
```bash
cd ai-module
python multi_camera_surveillance.py
```

### Step 4: Open Dashboard
```
http://localhost:5500/frontend/dashboard.html
```

## How It Works

### 1. Camera Configuration (Database)
Cameras are stored in MongoDB:
```javascript
{
  cameraId: "cam01",
  name: "Main Gate Camera",
  location: "Front Entrance",
  streamUrl: "http://192.168.1.20:8080/video",
  status: "active"
}
```

### 2. Multi-Camera Processing (Python)
```python
# Loads cameras from API
cameras = fetch_from_api('/api/cameras/active/list')

# Starts thread for each camera
for camera in cameras:
    thread = Thread(target=process_camera, args=(camera,))
    thread.start()
```

### 3. Detection Flow
```
Camera Stream → YOLO Detection → Face Match → Backend API → Dashboard Alert
```

### 4. Report Creation
When person detected:
```javascript
{
  person: ObjectId("..."),
  camera: ObjectId("..."),  // ← NEW: Links to camera
  detectionInfo: {
    cameraId: "cam01",
    cameraName: "Main Gate Camera",  // ← NEW
    cameraLocation: "Front Entrance", // ← NEW
    timestamp: "2025-10-29T20:35:00Z"
  }
}
```

## API Endpoints

### Get All Cameras
```bash
GET http://localhost:3000/api/cameras
```

### Get Active Cameras (for surveillance)
```bash
GET http://localhost:3000/api/cameras/active/list
```

### Add New Camera
```bash
POST http://localhost:3000/api/cameras
Content-Type: application/json

{
  "cameraId": "cam05",
  "name": "Back Door Camera",
  "location": "Building B - Back Entrance",
  "streamUrl": "http://192.168.1.60:8080/video",
  "status": "active"
}
```

### Update Camera Status
```bash
PATCH http://localhost:3000/api/cameras/cam01/status
Content-Type: application/json

{
  "status": "maintenance"
}
```

## Testing with Local Webcam

The seed script includes a local webcam camera:
```javascript
{
  cameraId: "cam_local",
  name: "Local Webcam",
  location: "Development Machine",
  streamUrl: "0"  // 0 = default webcam
}
```

## Dashboard View

Reports now display:
```
┌────────────────────────────────────────┐
│ 🔔 Person Identified                   │
│                                        │
│ John Doe - 87.5% Match                │
│ 📹 Main Gate Camera                    │
│ 📍 Front Entrance                      │
│ 🕐 Just now                            │
│                                        │
│ [✓ Confirm] [✗ False Positive]       │
└────────────────────────────────────────┘
```

## Files Created/Modified

### New Files:
1. `backend-api/models/Camera.js` - Camera model
2. `backend-api/routes/cameras.js` - Camera API routes
3. `backend-api/seed-cameras.js` - Database seeder
4. `ai-module/multi_camera_surveillance.py` - Multi-camera processor
5. `MULTI_CAMERA_SETUP.md` - Full documentation

### Modified Files:
1. `backend-api/server.js` - Added camera routes
2. `backend-api/models/Report.js` - Added camera reference
3. `backend-api/routes/recognition.js` - Links camera to reports
4. `backend-api/routes/reports.js` - Populates camera info
5. `frontend/js/reports.js` - Displays camera info

## Configuration

### Python Script Settings
Edit `ai-module/multi_camera_surveillance.py`:
```python
BACKEND_URL = 'http://localhost:3000'
YOLO_CONFIDENCE = 0.5
PROCESS_EVERY_N_FRAMES = 2
MATCH_COOLDOWN = 10
```

### Camera Stream URLs

**IP Camera:**
```
http://192.168.1.20:8080/video
```

**RTSP Stream:**
```
rtsp://admin:password@192.168.1.20:554/stream
```

**USB Webcam:**
```
0  (first webcam)
1  (second webcam)
```

**Phone Camera (IP Webcam app):**
```
http://192.168.1.100:8080/video
```

## Adding Your Own Cameras

### Method 1: API (Recommended)
Use Postman or curl:
```bash
curl -X POST http://localhost:3000/api/cameras \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "cameraId": "my_camera",
    "name": "My Camera",
    "location": "My Location",
    "streamUrl": "http://192.168.1.50:8080/video"
  }'
```

### Method 2: Seed Script
Edit `backend-api/seed-cameras.js` and add your cameras to the array.

### Method 3: MongoDB Direct
```javascript
db.cameras.insertOne({
  cameraId: "my_camera",
  name: "My Camera",
  location: "My Location",
  streamUrl: "http://192.168.1.50:8080/video",
  status: "active",
  isActive: true,
  createdAt: new Date()
})
```

## Verification Workflow

When person is detected:

1. **Alert Created** - Report with status "pending"
2. **Dashboard Shows** - Camera name, location, person name
3. **Operator Reviews** - Checks the detection
4. **Confirms/Rejects** - Clicks button
5. **Status Updated** - Report marked as "confirmed" or "false_positive"
6. **Person Status** - If confirmed, person status can be updated to "found"

## Performance Tips

### For Multiple Cameras:
- Increase `PROCESS_EVERY_N_FRAMES` to 3 or 4
- Use `yolov8n.pt` (fastest model)
- Consider GPU acceleration
- Monitor CPU/RAM usage

### For Better Accuracy:
- Use `yolov8s.pt` or `yolov8m.pt`
- Decrease `PROCESS_EVERY_N_FRAMES` to 1
- Ensure good lighting in camera views
- Use higher resolution streams

## Troubleshooting

### "No cameras configured"
- Run seed script: `node seed-cameras.js`
- Check backend is running
- Verify MongoDB connection

### "Failed to open stream"
- Check camera URL is correct
- Test URL in VLC player
- Verify network connectivity
- Check camera is powered on

### "No face encodings loaded"
- Add persons to database
- Upload face images
- Verify encodings are generated
- Check API connection

## Next Steps

1. ✅ System is ready to use
2. 🎥 Add your camera streams
3. 👤 Add persons to database
4. 🚀 Start surveillance
5. 📊 Monitor dashboard

## Support

Check the full documentation in `MULTI_CAMERA_SETUP.md` for:
- Detailed API reference
- Advanced configuration
- Security considerations
- Performance optimization
- Hardware requirements
