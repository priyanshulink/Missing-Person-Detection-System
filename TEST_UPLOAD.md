# Upload Error Troubleshooting Guide

## 🐛 Error: "Error adding person: [object Object]"

This error has been fixed with better error handling. Now you'll see the actual error message.

---

## ✅ What I Fixed

### 1. **Better Error Messages**
- Added detailed console logging
- Proper error message extraction
- Shows actual error instead of "[object Object]"

### 2. **Enhanced Logging**
- Backend logs each step of upload
- Frontend logs upload progress
- Python script errors are captured

---

## 🧪 How to Test

### Step 1: Open Browser Console
1. Open dashboard: http://localhost:8080
2. Press **F12** to open Developer Tools
3. Go to **Console** tab

### Step 2: Try Adding Person
1. Click "Persons" → "Add Person"
2. Fill in name and details
3. Click "Capture from Webcam" OR "Upload Photo"
4. Capture/select a photo
5. Click "Save Person"

### Step 3: Check Console
You should see detailed logs:
```
Uploading photo...
Upload response: {success: true, encoding: [...], ...}
Face encoding extracted successfully
Creating person with data: {...}
Person created: {...}
✅ Person added successfully with face encoding!
```

---

## 🔍 Common Errors & Solutions

### Error: "No face detected in image"

**Cause**: Photo doesn't have a clear face

**Solution**:
- Use a clear, front-facing photo
- Ensure good lighting
- Face should be clearly visible
- No sunglasses or masks
- Try capturing again

---

### Error: "Photo upload failed: Failed to fetch"

**Cause**: Backend not running or not accessible

**Solution**:
```powershell
# Check if backend is running
curl http://localhost:3000/health

# If not running, start it
cd backend-api
node server.js
```

---

### Error: "No file uploaded"

**Cause**: Photo not captured/selected properly

**Solution**:
- Make sure you clicked "Capture Photo" button
- Or selected a file when uploading
- Check that preview image appears
- Try again

---

### Error: "Python script failed"

**Cause**: Python dependencies missing or Python not found

**Solution**:
```powershell
# Check Python
python --version

# Install dependencies
pip install face_recognition opencv-python numpy

# Test face_recognition
python -c "import face_recognition; print('OK')"
```

---

### Error: "Failed to parse encoding result"

**Cause**: Python script output is malformed

**Solution**:
```powershell
# Test the extraction script manually
cd ai-module
python extract_encoding.py "path/to/test/image.jpg"

# Should output JSON like:
# {"success": true, "encoding": [...], ...}
```

---

## 📊 Backend Logs to Watch

When you upload a photo, backend should show:

```
📸 Photo upload request received
✅ File saved to: backend-api\uploads\person-1234567890.jpg
🔍 Extracting face encoding...
📊 Extraction result: { success: true, encoding: [...], ... }
✅ Face encoding extracted successfully
```

**If you see errors**, they will show exactly what went wrong.

---

## 🧪 Manual Test

### Test Photo Upload Directly

```powershell
# Get auth token first (login via dashboard, check browser console)
$token = "YOUR_TOKEN_HERE"

# Test upload
$headers = @{Authorization="Bearer $token"}
$filePath = "C:\path\to\photo.jpg"
$form = @{photo=Get-Item -Path $filePath}

Invoke-RestMethod -Uri "http://localhost:3000/api/upload/person-photo" -Method Post -Headers $headers -Form $form
```

**Expected response**:
```json
{
  "message": "Face encoding extracted successfully",
  "encoding": [0.123, 0.456, ...],
  "imageUrl": "/uploads/person-123456.jpg",
  "facesDetected": 1
}
```

---

## 🔧 Debug Checklist

- [ ] Backend server is running
- [ ] MongoDB is running
- [ ] Python is installed and accessible
- [ ] face_recognition package is installed
- [ ] opencv-python package is installed
- [ ] Browser has camera permissions (for webcam capture)
- [ ] Photo has a clear visible face
- [ ] Good lighting in photo
- [ ] Face is front-facing

---

## 📝 Check Backend Logs

After trying to add a person, check the backend terminal for:

**Success**:
```
📸 Photo upload request received
✅ File saved to: ...
🔍 Extracting face encoding...
✅ Face encoding extracted successfully
```

**Failure**:
```
📸 Photo upload request received
✅ File saved to: ...
🔍 Extracting face encoding...
❌ Face detection failed: No face detected in image
```

The error message will tell you exactly what went wrong!

---

## 🎯 Quick Fix Steps

1. **Refresh browser** (Ctrl+F5)
2. **Try with a different photo** (clear face, good lighting)
3. **Check backend terminal** for error messages
4. **Check browser console** (F12) for detailed logs
5. **Try uploading instead of capturing** (or vice versa)

---

## ✅ Success Indicators

**You know it's working when**:

1. ✅ Photo preview appears after capture/upload
2. ✅ No errors in browser console
3. ✅ Backend shows "Face encoding extracted successfully"
4. ✅ Alert shows "✅ Person added successfully with face encoding!"
5. ✅ Person appears in persons list
6. ✅ Person has face encoding count > 0

---

## 🚀 Next Steps

After successfully adding a person:

1. **Check persons list** - Person should appear
2. **Login/logout** - Surveillance restarts
3. **Show face to camera** - Should detect and alert
4. **Check reports** - Detection should be logged

---

**The error handling is now much better - you'll see exactly what's wrong!** 🎯
