# Camera Control Guide

## How to Start/Stop Library Hall Camera

### Method 1: Using Batch Script (Easiest)

**List all cameras:**
```bash
camera_control.bat list
```

**Start Library Hall Camera:**
```bash
camera_control.bat start cam02
```

**Stop Library Hall Camera:**
```bash
camera_control.bat stop cam02
```

**Check camera status:**
```bash
camera_control.bat status cam02
```

### Method 2: Using Python Script

**List all cameras:**
```bash
python control_camera.py list
```

**Start Library Hall Camera:**
```bash
python control_camera.py start cam02
```

**Stop Library Hall Camera:**
```bash
python control_camera.py stop cam02
```

**Check camera status:**
```bash
python control_camera.py status cam02
```

### Method 3: Using API Directly (curl)

**Start camera:**
```bash
curl -X PATCH http://localhost:3000/api/cameras/cam02/status ^
  -H "Content-Type: application/json" ^
  -d "{\"status\": \"active\"}"
```

**Stop camera:**
```bash
curl -X PATCH http://localhost:3000/api/cameras/cam02/status ^
  -H "Content-Type: application/json" ^
  -d "{\"status\": \"inactive\"}"
```

### Method 4: Using Postman/Thunder Client

**Endpoint:** `PATCH http://localhost:3000/api/cameras/cam02/status`

**Start camera - Body:**
```json
{
  "status": "active"
}
```

**Stop camera - Body:**
```json
{
  "status": "inactive"
}
```

## Camera Status Values

- **`active`** - Camera is running and processing
- **`inactive`** - Camera is stopped
- **`maintenance`** - Camera is under maintenance

## How It Works

### Starting a Camera

1. **Update Status** in database to `active`
2. **Multi-camera system** detects active cameras
3. **Creates thread** for the camera
4. **Starts processing** stream

### Stopping a Camera

1. **Update Status** in database to `inactive`
2. **Multi-camera system** skips inactive cameras
3. **Thread stops** processing
4. **Resources released**

## Quick Reference

### Library Hall Camera
- **Camera ID:** `cam02`
- **Name:** Library Hall Camera
- **Location:** Library First Floor
- **Stream URL:** http://10.28.71.10:8080/video

### Commands

```bash
# List all cameras
camera_control.bat list

# Start Library Hall Camera
camera_control.bat start cam02

# Stop Library Hall Camera
camera_control.bat stop cam02

# Check status
camera_control.bat status cam02
```

## Expected Output

### Starting Camera
```
Starting camera: cam02
✅ Camera 'cam02' activated successfully

Camera: Library Hall Camera
Location: Library First Floor
Status: active
```

### Stopping Camera
```
Stopping camera: cam02
✅ Camera 'cam02' deactivated successfully

Camera: Library Hall Camera
Location: Library First Floor
Status: inactive
```

### Listing Cameras
```
📹 Available Cameras:
----------------------------------------------------------------------
🟢 cam02           | Library Hall Camera       | active
🔴 cam01           | Main Gate Camera          | inactive
🟢 cam_local       | Local Webcam              | active
----------------------------------------------------------------------
```

## Important Notes

### 1. Backend Must Be Running
Before controlling cameras, ensure backend is running:
```bash
cd backend-api
npm start
```

### 2. Changes Take Effect Immediately
- Stopping a camera: Thread stops on next database check (~30 seconds)
- Starting a camera: Thread starts when multi-camera system reloads

### 3. Multi-Camera System
The multi-camera surveillance system automatically:
- Loads only `active` cameras
- Skips `inactive` cameras
- Refreshes camera list periodically

### 4. Restart Multi-Camera System
For immediate effect, restart the surveillance system:
```bash
# Stop current system (Ctrl+C)
# Then restart
python multi_camera_surveillance.py
```

## Troubleshooting

### Camera Won't Start
1. Check backend is running
2. Verify camera exists in database
3. Check stream URL is accessible
4. Test stream with `test_camera_stream.py`

### Camera Won't Stop
1. Check backend is running
2. Verify status update was successful
3. Restart multi-camera system if needed

### Status Not Updating
1. Check MongoDB connection
2. Verify camera ID is correct
3. Check API endpoint is accessible

## Advanced: Programmatic Control

### Python
```python
import requests

# Start camera
requests.patch(
    'http://localhost:3000/api/cameras/cam02/status',
    json={'status': 'active'}
)

# Stop camera
requests.patch(
    'http://localhost:3000/api/cameras/cam02/status',
    json={'status': 'inactive'}
)
```

### JavaScript
```javascript
// Start camera
fetch('http://localhost:3000/api/cameras/cam02/status', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'active' })
});

// Stop camera
fetch('http://localhost:3000/api/cameras/cam02/status', {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'inactive' })
});
```

## Integration with Dashboard

You can add camera control buttons to the frontend dashboard:

```html
<button onclick="startCamera('cam02')">Start Library Camera</button>
<button onclick="stopCamera('cam02')">Stop Library Camera</button>
```

```javascript
async function startCamera(cameraId) {
  await fetch(`/api/cameras/${cameraId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'active' })
  });
  alert('Camera started');
}

async function stopCamera(cameraId) {
  await fetch(`/api/cameras/${cameraId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'inactive' })
  });
  alert('Camera stopped');
}
```

## All Camera IDs

From your configuration:

| Camera ID | Name | Location |
|-----------|------|----------|
| cam01 | Main Gate Camera | Front Entrance |
| cam02 | Library Hall Camera | Library First Floor |
| cam03 | Parking Lot Camera | Building A Parking |
| cam04 | Cafeteria Camera | Ground Floor Cafeteria |
| cam_local | Local Webcam | Development Machine |

## Summary

**Easiest way to control Library Hall Camera:**

```bash
# Start
camera_control.bat start cam02

# Stop
camera_control.bat stop cam02

# Check status
camera_control.bat status cam02
```

That's it! The camera will start/stop processing in the multi-camera surveillance system.
