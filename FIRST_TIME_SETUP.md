# First Time Setup Guide

## ⚠️ IMPORTANT: Run This Before Starting System

### Step 1: Seed Cameras to Database

Before running `start_all.bat` for the first time, you MUST add cameras to the database:

```bash
cd backend-api
node seed-cameras.js
```

**Expected Output:**
```
✅ Connected to MongoDB
✅ Added camera: Main Gate Camera (cam01)
✅ Added camera: Library Hall Camera (cam02)
✅ Added camera: Parking Lot Camera (cam03)
✅ Added camera: Cafeteria Camera (cam04)
✅ Added camera: Local Webcam (cam_local)

✅ Camera seeding completed

📹 Total cameras in database: 5
  - Main Gate Camera (cam01) - Front Entrance [active]
  - Library Hall Camera (cam02) - Library First Floor [active]
  - Parking Lot Camera (cam03) - Building A Parking [active]
  - Cafeteria Camera (cam04) - Ground Floor Cafeteria [active]
  - Local Webcam (cam_local) - Development Machine [active]
```

### Step 2: Start the System

Now you can start everything:

```bash
cd ..
.\start_all.bat
```

### Step 3: Verify Cameras Loaded

Check the "Multi-Camera Surveillance" window. You should see:

```
✅ Loaded 5 active cameras

🚀 Starting surveillance on 5 cameras...

📹 Initialized camera: Main Gate Camera (cam01)
📹 Initialized camera: Library Hall Camera (cam02)
📹 Initialized camera: Parking Lot Camera (cam03)
📹 Initialized camera: Cafeteria Camera (cam04)
📹 Initialized camera: Local Webcam (cam_local)
```

## Troubleshooting

### "✅ Loaded 0 active cameras"

**Problem:** Cameras not in database

**Solution:**
```bash
cd backend-api
node seed-cameras.js
```

Then restart:
```bash
cd ..
.\stop_all.bat
.\start_all.bat
```

### "❌ No cameras configured"

**Problem:** Same as above - database is empty

**Solution:** Run seed script first

### Cameras Already Exist

If you run `seed-cameras.js` again, it will skip existing cameras:

```
⚠️  Camera cam01 already exists, skipping...
⚠️  Camera cam02 already exists, skipping...
```

To clear and reseed:
```bash
node seed-cameras.js --clear
```

## Complete First-Time Setup Checklist

- [ ] 1. Ensure MongoDB is running
- [ ] 2. Run `cd backend-api`
- [ ] 3. Run `node seed-cameras.js`
- [ ] 4. Verify cameras added (should see 5 cameras)
- [ ] 5. Run `cd ..`
- [ ] 6. Run `.\start_all.bat`
- [ ] 7. Check Multi-Camera window shows cameras loaded
- [ ] 8. Open browser: http://localhost:8080
- [ ] 9. Login and verify system working

## What Gets Seeded

### 5 Sample Cameras:

1. **cam01** - Main Gate Camera
   - Location: Front Entrance
   - URL: http://192.168.1.20:8080/video
   - Status: Active

2. **cam02** - Library Hall Camera
   - Location: Library First Floor
   - URL: http://10.28.71.10:8080/video
   - Status: Active

3. **cam03** - Parking Lot Camera
   - Location: Building A Parking
   - URL: http://192.168.1.45:8080/video
   - Status: Active

4. **cam04** - Cafeteria Camera
   - Location: Ground Floor Cafeteria
   - URL: http://192.168.1.50:8080/video
   - Status: Active

5. **cam_local** - Local Webcam
   - Location: Development Machine
   - URL: 0 (default webcam)
   - Status: Active

## After First Setup

After the first time, you only need:

```bash
.\start_all.bat
```

The cameras are already in the database and will load automatically.

## Editing Camera URLs

If you need to change camera URLs (like your Library Hall Camera):

### Option 1: Edit seed-cameras.js
Edit the file and change the URL:
```javascript
{
  cameraId: 'cam02',
  name: 'Library Hall Camera',
  location: 'Library First Floor',
  streamUrl: 'http://YOUR_NEW_IP:8080/video',  // ← Change this
  status: 'active'
}
```

Then reseed:
```bash
node seed-cameras.js --clear
```

### Option 2: Use API
```bash
curl -X PUT http://localhost:3000/api/cameras/cam02 ^
  -H "Content-Type: application/json" ^
  -d "{\"streamUrl\": \"http://YOUR_NEW_IP:8080/video\"}"
```

### Option 3: Use Control Script
```bash
# Stop camera first
camera_control.bat stop cam02

# Update in database (use API or MongoDB)

# Start camera again
camera_control.bat start cam02
```

## Summary

**First Time Only:**
```bash
cd backend-api
node seed-cameras.js
cd ..
.\start_all.bat
```

**Every Time After:**
```bash
.\start_all.bat
```

That's it! 🚀
