# Multi-Camera Surveillance - Status Filter Fix

## Problem

You were running the **multi-camera surveillance system** which was loading ALL persons from the database, not just missing ones. This caused:

1. **Prince detected in console** - System correctly detected Prince
2. **Om Singh alert shown** - But Om Singh (who was marked as "found") was still in the database being matched

## Root Cause

The multi-camera surveillance files were using:
```python
response = requests.get(f'{API_URL}/api/persons')  # ❌ Loads ALL persons
```

Instead of:
```python
response = requests.get(f'{API_URL}/api/persons?status=missing&limit=1000')  # ✅ Only missing
```

## Files Fixed

Updated **4 surveillance files** to filter by status=missing:

1. ✅ `ai-module/multi_camera_surveillance.py`
2. ✅ `ai-module/yolo_integrated_surveillance.py`
3. ✅ `ai-module/auto_surveillance.py`
4. ✅ `ai-module/webcam_detection.py`

## What Changed

### Before:
```python
def load_persons_from_api(self):
    """Load persons with face encodings from API"""
    response = requests.get(f'{API_URL}/api/persons', timeout=10)
    # Loads ALL persons including found ones ❌
```

### After:
```python
def load_persons_from_api(self):
    """Load persons with face encodings from API (only missing persons)"""
    response = requests.get(f'{API_URL}/api/persons?status=missing&limit=1000', timeout=10)
    # Only loads missing persons ✅
```

## How to Test

1. **Stop the current surveillance system** (Ctrl+C)

2. **Restart it:**
   ```bash
   cd ai-module
   python multi_camera_surveillance.py
   ```

3. **Check console output:**
   ```
   🔄 Loading missing persons from database...
   ✅ Loaded 2 face encodings  # Should be lower now (Om Singh excluded)
   ```

4. **Verify:**
   - If Om Singh is marked as "found", he should NOT be in the count
   - Only persons with status="missing" will be detected

## Expected Behavior

### Scenario 1: Om Singh is "found"
```
Console: [Library Hall Camera] ✅ Loaded 2 face encodings
         (Om Singh NOT loaded)

When Om Singh appears:
- ❌ NO detection
- ❌ NO alert
```

### Scenario 2: Prince is "missing"
```
Console: [Library Hall Camera] ✅ Loaded 2 face encodings
         (Prince IS loaded)

When Prince appears:
- ✅ Detection: "prince detected (similarity: 76.44%)"
- ✅ Alert sent to dashboard
- ✅ Report created
```

## Why It Happened

You have **two different detection systems**:

1. **`yolov8-person-detector/main.py`** - Single camera (already fixed)
2. **`ai-module/multi_camera_surveillance.py`** - Multi-camera (just fixed now)

The multi-camera system wasn't updated with the status filter, so it was still loading everyone.

## All Detection Systems Now Updated

✅ `yolov8-person-detector/main.py` - Status filter + auto-reload
✅ `yolov8-person-detector/face_matcher.py` - Status filter + fallback
✅ `ai-module/multi_camera_surveillance.py` - Status filter
✅ `ai-module/yolo_integrated_surveillance.py` - Status filter
✅ `ai-module/auto_surveillance.py` - Status filter
✅ `ai-module/webcam_detection.py` - Status filter

## Next Steps

**Restart your surveillance system** and it will now:
- Only load missing persons
- Exclude found persons automatically
- Show correct person count in console
- Match only active missing persons
