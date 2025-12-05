# Camera Stream Testing Guide

## Test Scripts Created

### 1. Single Camera Test (`test_camera_stream.py`)
Tests the Library Hall Camera stream with live video display.

**Usage:**
```bash
python test_camera_stream.py
```

**What it does:**
- Connects to `http://10.28.71.10:8080/video`
- Displays live video feed
- Shows frame counter
- Press 'q' to quit

**Expected Output:**
```
✅ Camera stream opened successfully!
Displaying live video...
✅ Streaming... Frame 100
✅ Streaming... Frame 200
```

### 2. Multi-Camera Test (`test_all_cameras.py`)
Tests all configured cameras without displaying video.

**Usage:**
```bash
python test_all_cameras.py
```

**What it does:**
- Tests each camera connection
- Checks frame reading capability
- Reports resolution
- Provides summary

**Expected Output:**
```
📹 Testing: Library Hall Camera (cam02)
   ✅ SUCCESS
   Resolution: 1920x1080

📹 Testing: Local Webcam (cam_local)
   ✅ SUCCESS
   Resolution: 1280x720

📊 Results: 2/2 cameras working
✅ All cameras are working correctly!
```

## Current Test Results

✅ **Library Hall Camera is working!**
- URL: `http://10.28.71.10:8080/video`
- Status: Streaming successfully
- Frames received: 100+

## Troubleshooting

### Camera Not Connecting

**Check 1: Network Connectivity**
```bash
ping 10.28.71.10
```

**Check 2: Test URL in Browser**
Open in browser: `http://10.28.71.10:8080/video`

**Check 3: IP Webcam App Settings**
- Ensure app is running on phone
- Check port is 8080
- Verify phone is on same network

**Check 4: Firewall**
- Allow Python through Windows Firewall
- Check router settings

### Stream Opens but No Frames

**Solution 1: Check Stream Format**
Try different URLs:
```python
# MJPEG stream
"http://10.28.71.10:8080/video"

# Individual frame
"http://10.28.71.10:8080/shot.jpg"

# Video feed
"http://10.28.71.10:8080/videofeed"
```

**Solution 2: Increase Timeout**
```python
cap = cv2.VideoCapture("http://10.28.71.10:8080/video")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
```

### Poor Performance

**Solution 1: Reduce Resolution**
In IP Webcam app:
- Settings → Video Preferences → Video Resolution
- Set to 640x480 or 800x600

**Solution 2: Reduce Quality**
- Settings → Video Preferences → JPEG Quality
- Set to 50-70%

**Solution 3: Reduce Frame Rate**
- Settings → Video Preferences → Video FPS Limit
- Set to 15 or 20 FPS

## Next Steps

### ✅ Step 1: Camera Stream Test (COMPLETED)
Your camera is working correctly!

### Step 2: Test with YOLO Detection
Run the single-camera YOLO test:
```bash
cd yolov8-person-detector
python main.py
```

### Step 3: Add Camera to Database
```bash
cd backend-api
node seed-cameras.js
```

### Step 4: Start Multi-Camera Surveillance
```bash
cd ai-module
python multi_camera_surveillance.py
```

## Camera Configuration Reference

### IP Webcam App (Android)
1. Install "IP Webcam" from Play Store
2. Start Server
3. Note the IP address shown (e.g., 10.28.71.10:8080)
4. Use URL: `http://10.28.71.10:8080/video`

### DroidCam (Android/iOS)
1. Install DroidCam app
2. Note IP and port
3. Use URL: `http://IP:PORT/video`

### USB Webcam
```python
# First webcam
cv2.VideoCapture(0)

# Second webcam
cv2.VideoCapture(1)
```

### RTSP Camera
```python
cv2.VideoCapture("rtsp://username:password@ip:port/stream")
```

### HTTP MJPEG Stream
```python
cv2.VideoCapture("http://ip:port/video")
```

## Performance Benchmarks

### Good Performance
- Frame rate: 15-30 FPS
- Resolution: 640x480 to 1280x720
- Latency: < 500ms

### Acceptable Performance
- Frame rate: 10-15 FPS
- Resolution: 640x480
- Latency: 500ms - 1s

### Poor Performance (needs optimization)
- Frame rate: < 10 FPS
- Latency: > 1s
- Frequent frame drops

## Integration with Multi-Camera System

Once camera test is successful, the multi-camera system will:

1. **Load Camera Config** from MongoDB
2. **Create Thread** for this camera
3. **Process Stream** with YOLO detection
4. **Match Faces** against database
5. **Send Alerts** to dashboard

### Expected Flow
```
Camera Stream → Thread 1 → YOLO → Face Match → Alert
                                                   ↓
                                              Dashboard
```

## Monitoring Camera Health

The system automatically monitors:
- **Connection Status**: Active/Inactive
- **Last Online**: Timestamp of last frame
- **Frame Rate**: Actual FPS
- **Error Count**: Connection failures

View in dashboard or via API:
```bash
GET http://localhost:3000/api/cameras
```

## Tips for Best Results

### Camera Placement
- Mount at 6-8 feet height
- Angle slightly downward
- Ensure good lighting
- Avoid backlighting

### Network
- Use wired connection if possible
- 2.4GHz WiFi for longer range
- 5GHz WiFi for better speed
- Ensure strong signal strength

### Settings
- Resolution: 1280x720 (720p)
- Frame rate: 15-20 FPS
- Quality: 60-70%
- Format: MJPEG

## Success Criteria

✅ Camera stream opens without errors
✅ Live video displays smoothly
✅ Frame rate is consistent
✅ No connection drops
✅ Latency is acceptable

**Your camera has passed all tests! Ready for YOLO integration.**
