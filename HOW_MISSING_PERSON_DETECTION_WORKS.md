# 🎯 How Missing Person Detection & Alert System Works

## 📋 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMERA SURVEILLANCE                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Camera captures video frame (every frame)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. YOLO detects persons in frame                            │
│    - Draws bounding boxes around people                     │
│    - Gets coordinates (x1, y1, x2, y2)                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Extract face from detected person                        │
│    - Crop face region from bounding box                     │
│    - Convert to RGB                                         │
│    - Resize for faster processing                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Generate face encoding (128-dimensional vector)          │
│    - Uses face_recognition library                          │
│    - Creates unique "fingerprint" of the face               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Compare with MISSING persons database                    │
│    - Only compares with persons marked as "missing"         │
│    - Calculates similarity (0-1 scale)                      │
│    - Threshold: 0.6 (60% similarity required)               │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────┴───────┐
                    │               │
              Match Found?      No Match
                    │               │
                    ↓               ↓
            ┌───────────┐     Continue
            │ YES       │     Monitoring
            └───────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Check cooldown (prevent spam)                            │
│    - Wait 10 seconds between alerts for same person         │
│    - Prevents multiple alerts for same detection            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Send alert to backend API                                │
│    POST /api/recognition                                    │
│    {                                                         │
│      encoding: [128 numbers],                               │
│      metadata: {                                            │
│        camera_id, camera_name, camera_location,             │
│        timestamp, bbox, similarity, person_id, person_name  │
│      }                                                       │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Backend creates report in database                       │
│    - Saves detection details                                │
│    - Links to person and camera                             │
│    - Records timestamp and location                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Send real-time notification (Socket.io)                  │
│    io.emit('match_found', {...})                            │
│    - Instant notification to dashboard                      │
│    - Shows alert in Alerts section                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. Send push notification (Firebase)                       │
│     - Sends to mobile devices                               │
│     - Title: "Person Identified"                            │
│     - Body: "[Name] detected at [Location]"                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 11. Dashboard updates in real-time                          │
│     - Alerts section shows new alert                        │
│     - Reports section shows new report                      │
│     - Alert badge count increases                           │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Detailed Explanation

### Step 1: Load Missing Persons Database

**File:** `multi_camera_surveillance.py` (Line 60-91)

```python
def load_persons_from_api(self):
    # Only load persons with status=missing
    response = requests.get(f'{BACKEND_URL}/api/persons?status=missing&limit=1000')
    
    for person in persons:
        if person.get('faceEncodings'):
            # Store face encodings, names, and IDs
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(person.name)
            self.known_face_ids.append(person._id)
```

**Key Point:** Only persons marked as **"missing"** are loaded for comparison.

### Step 2: Detect Person with YOLO

**File:** `multi_camera_surveillance.py` (Line 93-110)

```python
def detect_persons_yolo(self, frame):
    results = self.yolo_model(frame)
    
    for detection in results[0].boxes:
        class_id = int(detection.cls[0])
        if class_id == 0:  # Person class
            bbox = detection.xyxy[0].cpu().numpy()
            confidence = float(detection.conf[0])
```

**Key Point:** YOLO detects **all persons** in frame, not just missing ones.

### Step 3: Extract and Match Face

**File:** `multi_camera_surveillance.py` (Line 126-171)

```python
def match_face(self, frame, bbox):
    # Extract face region
    face_region = frame[y1:y2, x1:x2]
    
    # Generate face encoding
    face_encoding = face_recognition.face_encodings(rgb_face)[0]
    
    # Compare with known faces
    face_distances = face_recognition.face_distance(
        self.known_face_encodings, 
        face_encoding
    )
    
    # Find best match
    best_match_index = np.argmin(face_distances)
    best_distance = face_distances[best_match_index]
    
    # Check threshold (0.6 = 60% similarity)
    if best_distance <= 0.6:
        similarity = 1 - best_distance
        return (
            self.known_face_names[best_match_index],
            self.known_face_ids[best_match_index],
            similarity
        )
```

**Key Point:** 
- Lower distance = Higher similarity
- Threshold: 0.6 (adjustable)
- Returns: Name, ID, Similarity score

### Step 4: Send Alert with Cooldown

**File:** `multi_camera_surveillance.py` (Line 173-207)

```python
def send_match_to_backend(self, person_name, person_id, similarity, bbox):
    # Check cooldown (10 seconds)
    if person_id in self.last_match_time:
        if current_time - self.last_match_time[person_id] < MATCH_COOLDOWN:
            return  # Skip - too soon
    
    # Prepare payload
    payload = {
        'encoding': [0] * 128,
        'metadata': {
            'camera_id': self.camera_id,
            'camera_name': self.camera_name,
            'camera_location': self.location,
            'timestamp': datetime.now().isoformat(),
            'bbox': {'x1': bbox[0], 'y1': bbox[1], 'x2': bbox[2], 'y2': bbox[3]},
            'detection_confidence': float(similarity),
            'person_id': person_id,
            'person_name': person_name
        }
    }
    
    # Send to backend
    response = requests.post(f'{BACKEND_URL}/api/recognition', json=payload)
    
    if response.status_code == 200:
        print(f"🚨 ALERT: {person_name} detected (similarity: {similarity:.2%})")
```

**Key Point:** 
- Cooldown prevents spam (10 seconds between alerts for same person)
- Sends detailed metadata to backend

### Step 5: Backend Creates Report

**File:** `backend-api/routes/recognition.js` (Line 116-147)

```javascript
// Create report
const reportData = {
  person: bestMatch._id,
  matchDetails: {
    similarity: bestSimilarity,
    confidence: metadata?.detection_confidence || 0,
    faceEncoding: encoding
  },
  detectionInfo: {
    cameraId: metadata?.camera_id,
    cameraName: camera?.name,
    cameraLocation: camera?.location,
    timestamp: new Date(metadata.timestamp),
    bbox: metadata?.bbox
  },
  alertSent: false
};

const report = new Report(reportData);
await report.save();
```

**Key Point:** Report stored in database with all detection details.

### Step 6: Send Real-Time Notification

**File:** `backend-api/routes/recognition.js` (Line 149-162)

```javascript
// Send Socket.io notification
const io = req.app.get('io');
if (io) {
  io.emit('match_found', {
    reportId: report._id,
    personId: bestMatch._id,
    personName: bestMatch.name,
    similarity: bestSimilarity,
    cameraId: metadata?.camera_id,
    cameraName: metadata?.camera_name,
    cameraLocation: metadata?.camera_location,
    timestamp: report.detectionInfo.timestamp
  });
}
```

**Key Point:** Socket.io sends instant notification to all connected dashboards.

### Step 7: Send Push Notification

**File:** `backend-api/routes/recognition.js` (Line 164-191)

```javascript
// Send Firebase Cloud Messaging notification
await sendNotification({
  title: 'Person Identified',
  body: `${bestMatch.name} detected with ${(bestSimilarity * 100).toFixed(1)}% similarity at ${cameraLocation}`,
  data: {
    reportId: report._id.toString(),
    personId: bestMatch._id.toString(),
    personName: bestMatch.name,
    similarity: bestSimilarity.toString(),
    cameraName: cameraName,
    cameraLocation: cameraLocation
  }
});
```

**Key Point:** Push notification sent to mobile devices.

## ⚙️ Configuration

### Similarity Threshold

**File:** `multi_camera_surveillance.py` (Line 159)

```python
if best_distance <= 0.6:  # Tolerance
```

**Adjust threshold:**
- `0.4` = Very strict (fewer false positives, may miss some matches)
- `0.6` = Balanced (default)
- `0.8` = Lenient (more matches, more false positives)

### Alert Cooldown

**File:** `multi_camera_surveillance.py` (Line 34)

```python
MATCH_COOLDOWN = 10  # seconds between alerts for same person
```

**Adjust cooldown:**
- `5` = More frequent alerts
- `10` = Default
- `30` = Less frequent alerts

### Frame Processing Rate

**File:** `multi_camera_surveillance.py` (Line 33)

```python
PROCESS_EVERY_N_FRAMES = 3  # Process every 3rd frame
```

**Adjust processing:**
- `1` = Every frame (slower, more accurate)
- `3` = Every 3rd frame (balanced)
- `5` = Every 5th frame (faster, less accurate)

## 📊 Example Scenario

### Setup:
- **Missing Person:** John Doe (added to database with status="missing")
- **Camera:** Front Door Camera (active)
- **Surveillance:** Running

### Timeline:

```
10:00:00 - John Doe walks in front of camera
10:00:00 - YOLO detects person
10:00:00 - Face extracted and encoded
10:00:00 - Compared with missing persons database
10:00:00 - Match found: John Doe (87% similarity)
10:00:00 - Alert sent to backend
10:00:01 - Report created in database
10:00:01 - Socket.io notification sent to dashboard
10:00:01 - Push notification sent to mobile
10:00:01 - Dashboard shows alert: "John Doe detected at Front Door"
10:00:01 - Console: "🚨 ALERT: John Doe detected (similarity: 87.00%)"

10:00:05 - John Doe still in frame
10:00:05 - Detected again but cooldown active
10:00:05 - No new alert sent (preventing spam)

10:00:15 - John Doe still in frame
10:00:15 - Cooldown expired (10 seconds passed)
10:00:15 - New alert sent
```

## 🎯 Why Only Missing Persons?

The system is designed to **only alert for missing persons** because:

1. **Privacy:** Don't track everyone, only those who need to be found
2. **Performance:** Fewer comparisons = faster processing
3. **Relevance:** Only send alerts that matter
4. **Database Size:** Smaller database = faster matching

## 🔧 How to Add a Missing Person

1. **Login to dashboard**
2. **Go to Persons section**
3. **Click "Add Person"**
4. **Fill in details:**
   - Name
   - Age
   - Description
   - **Status: "missing"** ← Important!
5. **Upload photo(s)**
6. **Save**

The surveillance system will:
- Reload persons every 30 seconds
- Start comparing faces with new person
- Send alerts if detected

## 📋 Summary

### Detection Flow:
1. ✅ Camera captures frame
2. ✅ YOLO detects person
3. ✅ Extract face
4. ✅ Compare with missing persons only
5. ✅ If match → Send alert
6. ✅ Backend creates report
7. ✅ Send notifications
8. ✅ Dashboard updates

### Key Features:
- ✅ Only alerts for missing persons
- ✅ Adjustable similarity threshold
- ✅ Cooldown prevents spam
- ✅ Real-time notifications
- ✅ Mobile push notifications
- ✅ Detailed reports with location and timestamp

---

**The system is designed to help find missing persons quickly and efficiently!** 🎯✨
