# Camera Name and Location Feature

## Overview
Added camera name and location tracking to the surveillance system. When a person is detected, the system now displays:
- **Camera Name**: Identifies which camera detected the person
- **Camera Location**: Shows the physical location of the camera

## Changes Made

### 1. Configuration Files

#### `yolov8-person-detector/config.py`
```python
CAMERA_NAME = 'Main Entrance Camera'  # Name of the camera
CAMERA_LOCATION = 'Building A - Main Entrance'  # Physical location of the camera
```

#### `yolov8-person-detector/main.py`
```python
CAMERA_NAME = 'Main Entrance Camera'
CAMERA_LOCATION = 'Building A - Main Entrance'
```

#### `ai-module/yolo_integrated_surveillance.py`
```python
CAMERA_NAME = 'Main Entrance Camera'
CAMERA_LOCATION = 'Building A - Main Entrance'
```

### 2. Alert System Updates

#### `yolov8-person-detector/alert_system.py`
- Updated `trigger_alert()` to accept `camera_name` and `camera_location` parameters
- Updated `draw_alert_banner()` to display camera info on video feed
- Alert messages now include: `Camera: [name] | Location: [location]`

#### `yolov8-person-detector/main.py`
- Passes camera info to `alert_system.trigger_alert()`
- Passes camera info to `alert_system.draw_alert_banner()`

### 3. Backend API Updates

#### `backend-api/models/Report.js`
Added new fields to `detectionInfo`:
```javascript
cameraName: {
  type: String,
  default: 'Unknown Camera'
},
cameraLocation: {
  type: String,
  default: 'Unknown Location'
}
```

#### `backend-api/routes/recognition.js`
- Stores camera name and location in reports
- Includes camera info in Socket.io notifications
- Includes camera location in FCM push notifications

### 4. Frontend Updates

#### `frontend/js/alerts.js`
- Displays camera name and location in alert cards
- Shows camera info with icons:
  - 📹 Camera name (bold)
  - 📍 Camera location
- Browser notifications include camera location

## How to Configure

### For Standalone Detection (main.py)
Edit `yolov8-person-detector/main.py`:
```python
CAMERA_NAME = 'Your Camera Name'
CAMERA_LOCATION = 'Your Camera Location'
```

### For Integrated Surveillance (yolo_integrated_surveillance.py)
Edit `ai-module/yolo_integrated_surveillance.py`:
```python
CAMERA_NAME = 'Your Camera Name'
CAMERA_LOCATION = 'Your Camera Location'
```

### For Multiple Cameras
If you have multiple cameras, you can:
1. Create separate configuration files for each camera
2. Pass camera info as command-line arguments
3. Use environment variables

## Example Output

### Console Alert
```
============================================================
🚨 [2025-10-29 20:35:00] ALERT: John Doe detected (confidence: 87.5%) | Camera: Main Entrance Camera | Location: Building A - Main Entrance
============================================================
```

### Video Feed Banner
```
┌─────────────────────────────────────────────────────────┐
│ ALERT: John Doe DETECTED!                               │
│ Confidence: 87.5%                                       │
│ Camera: Main Entrance Camera    Location: Building A   │
└─────────────────────────────────────────────────────────┘
```

### Dashboard Alert
```
🔔 Person Identified
John Doe detected with 87.5% similarity
📹 Main Entrance Camera
📍 Building A - Main Entrance
```

### Push Notification
```
Person Identified
John Doe detected with 87.5% similarity at Building A - Main Entrance
```

## Benefits

1. **Better Tracking**: Know exactly which camera detected the person
2. **Faster Response**: Security can quickly identify the location
3. **Audit Trail**: Reports include camera information for investigations
4. **Multi-Camera Support**: Essential for systems with multiple cameras
5. **Improved Alerts**: More context in notifications and alerts

## Testing

1. Start the surveillance system
2. When a person is detected, verify:
   - Console shows camera name and location
   - Video feed banner displays camera info
   - Dashboard alerts include camera details
   - Push notifications mention the location

## Notes

- Camera name and location are configurable per camera
- Default values are used if not specified
- All existing functionality remains unchanged
- Camera info is stored in the database for historical tracking
