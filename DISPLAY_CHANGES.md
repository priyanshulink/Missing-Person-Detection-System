# Display Changes: Camera Name Instead of ID

## What Was Changed

Updated the dashboard to display **camera names** instead of **camera IDs**.

### Before
```
📹 cam02
🕐 2025-10-29 21:30:00
```

### After
```
📹 Library Hall Camera
📍 Library First Floor
🕐 2025-10-29 21:30:00
```

## Files Modified

### `frontend/js/dashboard.js`
- Changed from showing `cameraId` to showing `cameraName`
- Added camera location display
- Falls back to `cameraName` from detectionInfo if camera object not populated

## Display Locations

### 1. Dashboard - Recent Matches
Shows:
- **Camera Name** (bold) - e.g., "Library Hall Camera"
- **Camera Location** - e.g., "Library First Floor"
- Timestamp

### 2. Alerts Panel
Already showing:
- **Camera Name** (bold)
- **Camera Location**
- Timestamp

### 3. Reports Page
Already showing:
- **Camera Name** (bold)
- **Camera Location**
- Timestamp
- Status

## Example Display

### Dashboard Recent Matches
```
┌─────────────────────────────────────────────────┐
│ John Doe                          87.5%         │
│ 📹 Library Hall Camera                          │
│ 📍 Library First Floor                          │
│ 🕐 Just now                                     │
└─────────────────────────────────────────────────┘
```

### Alerts
```
┌─────────────────────────────────────────────────┐
│ 🔔 Person Identified                            │
│                                                 │
│ John Doe detected with 87.5% similarity         │
│ 📹 Library Hall Camera                          │
│ 📍 Library First Floor                          │
└─────────────────────────────────────────────────┘
```

### Reports
```
┌─────────────────────────────────────────────────┐
│ John Doe                          87.5% Match   │
│ 📹 Library Hall Camera                          │
│ 📍 Library First Floor                          │
│ 🕐 2025-10-29 21:30:00                          │
│ ✓ Status: pending                               │
│ [✓ Confirm] [✗ False Positive]                 │
└─────────────────────────────────────────────────┘
```

## Data Flow

### Backend Sends
```json
{
  "camera": {
    "_id": "...",
    "cameraId": "cam02",
    "name": "Library Hall Camera",
    "location": "Library First Floor"
  },
  "detectionInfo": {
    "cameraId": "cam02",
    "cameraName": "Library Hall Camera",
    "cameraLocation": "Library First Floor"
  }
}
```

### Frontend Displays
```javascript
// Priority order:
1. report.camera?.name           // From populated camera object
2. report.detectionInfo?.cameraName  // From detection metadata
3. 'Unknown Camera'              // Fallback
```

## Benefits

✅ **More User-Friendly**: "Library Hall Camera" vs "cam02"
✅ **Better Context**: Shows location immediately
✅ **Professional**: Looks more polished
✅ **Informative**: Users know exactly which camera detected the person

## Refresh to See Changes

After updating the code, refresh the dashboard:
1. Open http://localhost:8080
2. Press `Ctrl + F5` (hard refresh)
3. Or clear browser cache

## Testing

To verify the changes:

1. **Trigger a detection** on Library Hall Camera
2. **Check Dashboard** - Should show "Library Hall Camera"
3. **Check Alerts** - Should show "Library Hall Camera"
4. **Check Reports** - Should show "Library Hall Camera"

## Fallback Behavior

If camera object is not populated:
- Falls back to `detectionInfo.cameraName`
- If that's missing, shows "Unknown Camera"
- Never shows the camera ID to end users

## Camera Name Mapping

Current cameras in system:

| Camera ID | Display Name |
|-----------|--------------|
| cam01 | Main Gate Camera |
| cam02 | Library Hall Camera |
| cam03 | Parking Lot Camera |
| cam04 | Cafeteria Camera |
| cam_local | Local Webcam |

All displays now use the "Display Name" column instead of "Camera ID".
