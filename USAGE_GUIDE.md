# Status Feature Usage Guide

## Quick Start

### 1. Install Python Dependencies
```bash
cd yolov8-person-detector
pip install -r requirements.txt
```

### 2. Start Backend Server
```bash
cd backend-api
npm install  # if not already done
npm start    # starts on port 5000
```

### 3. Start Detection System
```bash
cd yolov8-person-detector
python main.py
```

## How It Works

### Adding a Missing Person
1. Open dashboard/frontend
2. Add person with photo
3. Person automatically gets `status: "missing"`
4. Detection system loads their face encoding

### When Person is Detected
1. Camera detects the person
2. System creates a report with match details
3. Report appears in dashboard as "pending"

### Confirming a Match (Marking as Found)
1. Authority reviews report in dashboard
2. Clicks **"Confirm"** button
3. System automatically:
   - ✅ Updates report status to "confirmed"
   - ✅ Updates person status to "found"
   - ✅ Shows "FOUND ✅" badge in dashboard
   - ✅ Person removed from active search on next reload

### Reloading Detection Database
**Automatic reload (every 30 seconds):**
- System automatically fetches fresh list of missing persons from API
- Found persons are excluded automatically
- No manual intervention needed

**Manual reload (immediate):**
- Press **'r'** key in the detection window for instant refresh

## Keyboard Controls (Detection System)

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Reload database (refresh missing persons from API) |
| `s` | Save screenshot |
| `c` | Clear alert cooldowns |

## API Endpoints

### Get Missing Persons Only
```bash
curl http://localhost:5000/api/persons?status=missing
```

### Update Person Status
```bash
curl -X PUT http://localhost:5000/api/persons/updateStatus/{person_id} \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "found"}'
```

## Status Values

| Status | Description |
|--------|-------------|
| `missing` | Person is being actively searched (default) |
| `found` | Person has been found, no longer searched |
| `active` | Person is in database but not missing |

## Troubleshooting

### Detection system not loading persons from API
**Problem:** Console shows "Could not connect to API server"

**Solution:**
1. Ensure backend is running on port 5000
2. Check `API_URL` in `yolov8-person-detector/config.py`
3. System will fall back to local `database/persons` folder

### Person still detected after marking as found
**Problem:** Found person still appears in detections

**Solution:**
1. Press **'r'** key in detection window to reload database
2. Verify person status in MongoDB is "found"
3. Check console output - person count should decrease

### Confirm button not working
**Problem:** Clicking Confirm doesn't update status

**Solution:**
1. Check browser console for errors
2. Verify user has admin/operator role
3. Check backend logs for authentication errors

## Configuration

### Change API URL
Edit `yolov8-person-detector/config.py`:
```python
API_URL = 'http://your-server:port'
```

### Change Backend Port
Edit `backend-api/.env` or `backend-api/server.js`:
```javascript
const PORT = process.env.PORT || 5000;
```

## Example Workflow

```
1. Missing Person Report
   └─> Person added to DB (status: "missing")
   └─> Detection system loads face encoding

2. Camera Detection
   └─> Person detected in camera feed
   └─> Alert triggered
   └─> Report created (status: "pending")

3. Authority Review
   └─> Opens dashboard
   └─> Reviews report details
   └─> Clicks "Confirm" button

4. System Updates
   └─> Report status → "confirmed"
   └─> Person status → "found"
   └─> Badge shows "FOUND ✅"

5. Detection System Update
   └─> Press 'r' to reload
   └─> Person removed from search list
   ### Why This Happens:

The Python detection system:
- Loads face encodings at startup
- Keeps them in memory for fast matching
- **Automatically reloads every 30 seconds** to check for database changes
- Can also be manually reloaded (press 'r') for immediate refresh

✅ **Automatic exclusion** - Found persons automatically excluded from search
✅ **Real-time updates** - Press 'r' to reload without restart
✅ **Visual feedback** - "FOUND ✅" badge in dashboard
✅ **API-driven** - Centralized database, no manual file management
✅ **Fallback support** - Works with local files if API unavailable
✅ **Performance** - Only searches for missing persons, faster processing
```

## Benefits

✅ **Automatic exclusion** - Found persons automatically excluded from search
✅ **Real-time updates** - Press 'r' to reload without restart
✅ **Visual feedback** - "FOUND ✅" badge in dashboard
✅ **API-driven** - Centralized database, no manual file management
✅ **Fallback support** - Works with local files if API unavailable
✅ **Performance** - Only searches for missing persons, faster processing
