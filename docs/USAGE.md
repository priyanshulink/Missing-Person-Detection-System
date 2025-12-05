# Usage Guide

## Starting the System

The system consists of 4 main components that need to be started in order:

### 1. Start MongoDB

```bash
# Windows
net start MongoDB

# Linux/Mac
sudo systemctl start mongodb
```

### 2. Start Backend API

```bash
cd backend-api
npm start
```

The API will start on `http://localhost:3000`

**Expected Output**:
```
✅ Connected to MongoDB
✅ Firebase initialized
🚀 Server running on port 3000
```

### 3. Start AI/ML Module

```bash
cd ai-module
python main.py
```

**Expected Output**:
```
Starting AI/ML Module...
Loading YOLOv8 model: yolov8n.pt
YOLOv8 model loaded successfully
AI module running. Press 'q' to quit.
```

### 4. Start Camera Module (Optional)

If you want to run the camera module separately:

```bash
cd camera-module
python camera_service.py
```

### 5. Access Dashboard

Open your web browser and navigate to:
```
file:///c:/Users/91900/Downloads/project/frontend/index.html
```

Or serve via HTTP server:
```bash
cd frontend
python -m http.server 8080
```
Then visit: `http://localhost:8080`

## First Time Setup

### 1. Create Admin Account

**Option A: Via API**
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "fullName": "System Administrator",
    "role": "admin"
  }'
```

**Option B: Via Dashboard**
1. Open the frontend
2. Click "Register" (if implemented)
3. Fill in the registration form

### 2. Login

1. Open the dashboard
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click "Login"

### 3. Add Persons to Database

1. Navigate to "Persons" tab
2. Click "Add Person"
3. Fill in person details:
   - Name (required)
   - Age, Gender
   - Status (missing/found/active)
   - Priority (low/medium/high/critical)
   - Description
   - Last seen location
4. Click "Save Person"

### 4. Add Face Encodings

Face encodings can be added via API:

```bash
curl -X POST http://localhost:3000/api/persons/{PERSON_ID}/encodings \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "encoding": [0.1, 0.2, ...],  // 128-dimensional vector
    "imageUrl": "path/to/image.jpg"
  }'
```

## Using the System

### Dashboard View

The dashboard shows:
- **Total Persons**: Number of persons in database
- **Total Matches**: Number of detection reports
- **Pending Reports**: Reports awaiting verification
- **Critical Alerts**: High-priority matches
- **Recent Matches**: Latest 5 detections

### Persons Management

**View All Persons**:
- Navigate to "Persons" tab
- Use filters to search by status, priority
- Use search box to find specific persons

**Add New Person**:
1. Click "Add Person" button
2. Fill in the form
3. Submit

**Edit Person**:
1. Click "Edit" on person card
2. Modify details
3. Save changes

**View Person Details**:
- Click "View" on person card
- See full profile including face encodings

### Reports Management

**View Reports**:
- Navigate to "Reports" tab
- See all detection reports with:
  - Person name
  - Camera ID
  - Timestamp
  - Similarity score
  - Verification status

**Verify Reports**:
1. Find pending report
2. Click "Confirm" if match is correct
3. Click "False Positive" if incorrect

### Real-Time Alerts

**View Alerts**:
- Navigate to "Alerts" tab
- See real-time notifications
- Badge shows number of unread alerts

**Alert Notifications**:
- Browser notifications (if permitted)
- Sound alerts
- Dashboard updates via Socket.io

## Camera Configuration

### Configure Camera Sources

Edit `camera-module/config.json`:

```json
{
  "camera_sources": [
    0,                           // Webcam
    "rtsp://192.168.1.100:554",  // IP Camera
    "http://camera.local/stream" // HTTP Stream
  ],
  "frame_width": 640,
  "frame_height": 480,
  "fps": 30
}
```

### Supported Camera Types

1. **USB/Webcam**: Use index (0, 1, 2, etc.)
2. **RTSP Stream**: `rtsp://username:password@ip:port/path`
3. **HTTP Stream**: `http://ip:port/video`
4. **Video File**: `/path/to/video.mp4`

## AI Module Configuration

Edit `ai-module/config.json`:

```json
{
  "backend_api_url": "http://localhost:3000",
  "confidence_threshold": 0.6,
  "yolo_model": "yolov8n.pt",
  "face_detection_model": "hog",
  "processing_fps": 5
}
```

**Parameters**:
- `confidence_threshold`: Minimum confidence for person detection (0-1)
- `yolo_model`: YOLOv8 model variant (n/s/m/l/x)
- `face_detection_model`: "hog" (faster) or "cnn" (more accurate)
- `processing_fps`: Frames to process per second

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Persons
- `GET /api/persons` - List all persons
- `GET /api/persons/:id` - Get person details
- `POST /api/persons` - Create person
- `PUT /api/persons/:id` - Update person
- `DELETE /api/persons/:id` - Delete person

### Recognition
- `POST /api/recognize` - Submit face encoding for matching

### Reports
- `GET /api/reports` - List all reports
- `GET /api/reports/:id` - Get report details
- `PATCH /api/reports/:id/verify` - Verify report

## Monitoring

### Check System Health

```bash
curl http://localhost:3000/health
```

**Response**:
```json
{
  "status": "OK",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "mongodb": "connected"
}
```

### View Logs

**Backend Logs**:
- Console output shows all API requests
- Morgan middleware logs HTTP requests

**AI Module Logs**:
- Console shows detection events
- Face recognition results
- API communication status

## Troubleshooting

### No detections appearing
1. Check AI module is running
2. Verify camera feed is working
3. Check backend API is accessible
4. Review confidence threshold settings

### False positives
1. Increase `confidence_threshold` in AI config
2. Add more face encodings per person
3. Use better quality reference images

### Slow performance
1. Reduce `processing_fps` in AI config
2. Use smaller YOLOv8 model (yolov8n)
3. Lower camera resolution
4. Use GPU acceleration if available

### Socket.io not connecting
1. Check backend is running
2. Verify CORS settings
3. Check firewall rules
4. Try different transport methods

## Best Practices

1. **Add Multiple Face Encodings**: Add 3-5 different photos per person for better accuracy
2. **Regular Verification**: Review and verify reports regularly
3. **Adjust Thresholds**: Fine-tune confidence thresholds based on your use case
4. **Monitor Performance**: Keep an eye on CPU/GPU usage
5. **Backup Database**: Regularly backup MongoDB data
6. **Update Models**: Keep YOLOv8 and face_recognition libraries updated

## Security Recommendations

1. Change default JWT secret in `.env`
2. Use strong passwords for admin accounts
3. Enable HTTPS in production
4. Restrict API access with firewall rules
5. Regularly update dependencies
6. Use environment variables for sensitive data
7. Implement rate limiting for API endpoints
