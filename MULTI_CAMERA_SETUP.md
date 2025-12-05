# Multi-Camera Surveillance System Setup Guide

## Overview
This system supports multiple camera streams processing simultaneously with centralized monitoring and alerting.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Multi-Camera System                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Camera 1 (Thread 1) ──┐                                   │
│  Camera 2 (Thread 2) ──┼──> YOLO Detection ──> Face Match  │
│  Camera 3 (Thread 3) ──┤                                   │
│  Camera N (Thread N) ──┘                                   │
│                                                              │
│                    ↓                                        │
│              Backend API                                    │
│           (MongoDB + Socket.io)                             │
│                    ↓                                        │
│            Dashboard + Alerts                               │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### 1. Database Setup

#### Add Camera Model
The Camera model is already created at `backend-api/models/Camera.js`

#### Seed Sample Cameras
```bash
cd backend-api
node seed-cameras.js
```

To clear existing cameras and reseed:
```bash
node seed-cameras.js --clear
```

### 2. Configure Cameras

#### Option A: Via API (Recommended)
Use the camera management endpoints:

**Create Camera:**
```bash
POST /api/cameras
{
  "cameraId": "cam01",
  "name": "Main Gate Camera",
  "location": "Front Entrance",
  "streamUrl": "http://192.168.1.20:8080/video",
  "status": "active"
}
```

**Get All Cameras:**
```bash
GET /api/cameras
```

**Get Active Cameras:**
```bash
GET /api/cameras/active/list
```

**Update Camera:**
```bash
PUT /api/cameras/cam01
{
  "name": "Updated Camera Name",
  "status": "maintenance"
}
```

#### Option B: Direct MongoDB
```javascript
db.cameras.insertOne({
  cameraId: "cam01",
  name: "Main Gate Camera",
  location: "Front Entrance",
  streamUrl: "http://192.168.1.20:8080/video",
  status: "active",
  isActive: true,
  createdAt: new Date()
})
```

### 3. Camera Stream URLs

#### IP Camera
```
http://192.168.1.20:8080/video
rtsp://admin:password@192.168.1.20:554/stream
```

#### USB Webcam
```
0  (for default webcam)
1  (for second webcam)
```

#### Phone Camera (IP Webcam App)
```
http://192.168.1.100:8080/video
```

#### RTSP Stream
```
rtsp://username:password@ip:port/path
```

### 4. Start Multi-Camera Surveillance

```bash
cd ai-module
python multi_camera_surveillance.py
```

The system will:
1. Load camera configurations from the database
2. Initialize YOLO model (shared across cameras)
3. Start a separate thread for each active camera
4. Process streams simultaneously
5. Send alerts to the backend

### 5. Monitor System

#### Check Camera Status
```bash
GET /api/cameras
```

Response shows:
- Active cameras
- Last online timestamp
- Current status

#### View Reports
```bash
GET /api/reports
```

Reports include:
- Person detected
- Camera name and location
- Detection timestamp
- Similarity score
- Verification status

## Camera Configuration Examples

### Example 1: Office Building
```json
[
  {
    "cameraId": "office_entrance",
    "name": "Main Office Entrance",
    "location": "Building A - Ground Floor",
    "streamUrl": "http://192.168.1.10:8080/video"
  },
  {
    "cameraId": "office_parking",
    "name": "Parking Lot Camera",
    "location": "Building A - Parking Area",
    "streamUrl": "http://192.168.1.11:8080/video"
  },
  {
    "cameraId": "office_lobby",
    "name": "Lobby Camera",
    "location": "Building A - Main Lobby",
    "streamUrl": "http://192.168.1.12:8080/video"
  }
]
```

### Example 2: Campus
```json
[
  {
    "cameraId": "campus_gate1",
    "name": "North Gate Camera",
    "location": "North Entrance",
    "streamUrl": "rtsp://admin:pass@192.168.2.10:554/stream"
  },
  {
    "cameraId": "campus_library",
    "name": "Library Entrance",
    "location": "Library Building",
    "streamUrl": "rtsp://admin:pass@192.168.2.20:554/stream"
  },
  {
    "cameraId": "campus_cafeteria",
    "name": "Cafeteria Camera",
    "location": "Student Center",
    "streamUrl": "rtsp://admin:pass@192.168.2.30:554/stream"
  }
]
```

## Features

### 1. Threaded Processing
- Each camera runs in its own thread
- Independent processing prevents blocking
- Shared YOLO model for efficiency

### 2. Automatic Database Sync
- Reloads person database every 30 seconds
- Updates camera status periodically
- No restart needed when adding persons

### 3. Alert Cooldown
- Prevents duplicate alerts
- 10-second cooldown per person per camera
- Configurable in code

### 4. Real-time Dashboard
- Live alerts from all cameras
- Camera name and location displayed
- Verification workflow

### 5. Report Management
- Detailed detection reports
- Camera information included
- Verification status tracking

## API Endpoints

### Camera Management
```
GET    /api/cameras              # Get all cameras
GET    /api/cameras/:id          # Get single camera
POST   /api/cameras              # Create camera (auth required)
PUT    /api/cameras/:id          # Update camera (auth required)
DELETE /api/cameras/:id          # Delete camera (auth required)
PATCH  /api/cameras/:id/status   # Update status (for monitoring)
GET    /api/cameras/active/list  # Get active cameras
```

### Recognition
```
POST   /api/recognize            # Face recognition endpoint
```

Payload:
```json
{
  "encoding": [128-dim array],
  "metadata": {
    "camera_id": "cam01",
    "camera_name": "Main Gate Camera",
    "camera_location": "Front Entrance",
    "timestamp": "2025-10-29T20:00:00Z",
    "bbox": {"x1": 100, "y1": 100, "x2": 300, "y2": 300}
  }
}
```

### Reports
```
GET    /api/reports              # Get all reports
GET    /api/reports/:id          # Get single report
PATCH  /api/reports/:id/verify   # Verify report
```

## Dashboard Display

Reports now show:

```
┌─────────────────────────────────────────────────────────┐
│ Person: John Doe                    87.5% Match         │
│ 📹 Main Gate Camera                                     │
│ 📍 Building A - Front Entrance                          │
│ 🕐 2025-10-29 20:35:00                                  │
│ ✓ Status: pending                                       │
│                                                          │
│ [✓ Confirm]  [✗ False Positive]                        │
└─────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Camera Not Connecting
1. Check stream URL is accessible
2. Verify network connectivity
3. Check camera credentials
4. Test stream with VLC player

### No Detections
1. Verify persons are in database
2. Check face encodings exist
3. Adjust confidence threshold
4. Verify YOLO model is loaded

### High CPU Usage
1. Increase `PROCESS_EVERY_N_FRAMES`
2. Reduce camera resolution
3. Use fewer cameras simultaneously
4. Optimize YOLO model (use yolov8n)

### Memory Issues
1. Limit number of cameras
2. Reduce frame processing rate
3. Clear old reports periodically
4. Monitor system resources

## Performance Optimization

### Recommended Settings

**For 1-2 Cameras:**
```python
PROCESS_EVERY_N_FRAMES = 1
YOLO_MODEL = 'yolov8n.pt'
```

**For 3-5 Cameras:**
```python
PROCESS_EVERY_N_FRAMES = 2
YOLO_MODEL = 'yolov8n.pt'
```

**For 6+ Cameras:**
```python
PROCESS_EVERY_N_FRAMES = 3
YOLO_MODEL = 'yolov8n.pt'
# Consider using GPU
```

### Hardware Requirements

**Minimum (1-2 cameras):**
- CPU: 4 cores
- RAM: 8 GB
- Storage: 20 GB

**Recommended (3-5 cameras):**
- CPU: 8 cores
- RAM: 16 GB
- GPU: NVIDIA GTX 1060 or better
- Storage: 50 GB

**High-end (6+ cameras):**
- CPU: 16 cores
- RAM: 32 GB
- GPU: NVIDIA RTX 3060 or better
- Storage: 100 GB

## Security Considerations

1. **Camera Credentials**: Store securely, use environment variables
2. **API Authentication**: Enable for camera management endpoints
3. **Network Security**: Use VPN for remote cameras
4. **Data Privacy**: Encrypt stored face encodings
5. **Access Control**: Limit dashboard access to authorized users

## Maintenance

### Regular Tasks
1. Clean old reports (monthly)
2. Update person database
3. Check camera status
4. Monitor system resources
5. Backup database

### Camera Health Monitoring
The system automatically updates camera status:
- `lastOnline` timestamp updated every 30 seconds
- Status can be: `active`, `inactive`, `maintenance`

## Next Steps

1. **Add More Cameras**: Use the API or seed script
2. **Configure Alerts**: Set up email/SMS notifications
3. **Customize UI**: Modify dashboard to show camera grid
4. **Add Recording**: Implement video recording on detection
5. **Analytics**: Add detection statistics and reports

## Support

For issues or questions:
1. Check logs in console output
2. Verify camera configurations
3. Test individual components
4. Review API responses
