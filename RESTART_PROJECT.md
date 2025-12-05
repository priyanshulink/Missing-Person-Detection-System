# Complete Project Restart Guide

**How to start all functionality from scratch**

---

## 🚀 Quick Start (Easiest Way)

### **Double-click**: `START_ALL.bat`

This will:
1. ✅ Check/Start MongoDB
2. ✅ Start Backend API (port 3000)
3. ✅ Start Frontend (port 8080)
4. ✅ Open dashboard in browser
5. ✅ Ready to use!

---

## 📋 Manual Start (Step by Step)

### Step 1: Start MongoDB

**Check if running**:
```powershell
sc query MongoDB
```

**If not running**:
```powershell
net start MongoDB
```

---

### Step 2: Start Backend API

```powershell
cd backend-api
node server.js
```

**Expected output**:
```
✅ Connected to MongoDB
✅ Firebase initialization skipped
🚀 Server running on port 3000
```

**Keep this terminal open!**

---

### Step 3: Start Frontend

**Open new terminal**:
```powershell
cd frontend
python -m http.server 8080
```

**Expected output**:
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

**Keep this terminal open!**

---

### Step 4: Open Dashboard

**Browser**: http://localhost:8080

**Login**:
- Username: `ompriyanshu12@gmail.com`
- Password: `pradeep3133`

**✅ Surveillance starts automatically on login!**

---

## 🎯 What Happens on Login

```
1. Login to Dashboard
        ↓
2. Backend receives login request
        ↓
3. Backend auto-starts surveillance
        ↓
4. Python surveillance script launches
        ↓
5. YOLOv8 + Face Recognition starts
        ↓
6. Webcam monitoring begins
        ↓
7. System ready to detect persons!
```

---

## 🔧 Verify Everything is Running

### Check Services

```powershell
# Check MongoDB
sc query MongoDB

# Check if backend is running
curl http://localhost:3000/health

# Check if frontend is accessible
curl http://localhost:8080
```

### Expected Results

| Service | Status | URL |
|---------|--------|-----|
| MongoDB | Running | mongodb://localhost:27017 |
| Backend API | Running | http://localhost:3000 |
| Frontend | Running | http://localhost:8080 |
| Surveillance | Auto-starts on login | - |

---

## 📊 System Status Check

### Backend Health Check

```powershell
curl http://localhost:3000/health
```

**Expected response**:
```json
{
  "status": "OK",
  "timestamp": "2025-10-12T...",
  "mongodb": "connected"
}
```

### Surveillance Status

**After login**, check:
```powershell
# Replace YOUR_TOKEN with actual token from login
curl http://localhost:3000/api/surveillance/status -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected response**:
```json
{
  "status": "running",
  "pid": 12345
}
```

---

## 🎮 Complete Functionality Test

### Test 1: Login ✅
1. Open http://localhost:8080
2. Login with credentials
3. Should see dashboard

### Test 2: Add Person with Webcam ✅
1. Click "Persons" tab
2. Click "Add Person"
3. Click "Capture from Webcam"
4. Webcam should open in browser
5. Capture photo
6. Fill details and save
7. Person should appear in list

### Test 3: Surveillance Detection ✅
1. After login, surveillance runs automatically
2. Show person's photo to webcam
3. Alert should appear in dashboard
4. Report should be created

### Test 4: View Reports ✅
1. Click "Reports" tab
2. Should see detection reports
3. Can filter by status, date, etc.

### Test 5: View Alerts ✅
1. Click "Alerts" tab
2. Should see real-time alerts
3. Shows recent detections

---

## 🛑 How to Stop Everything

### **Quick Stop**: Double-click `STOP_ALL.bat`

### **Manual Stop**:

**Stop Backend**:
- Go to backend terminal
- Press `Ctrl+C`

**Stop Frontend**:
- Go to frontend terminal
- Press `Ctrl+C`

**Stop Surveillance**:
- Automatically stops when backend stops
- Or manually: Close Python window

**Stop MongoDB** (optional):
```powershell
net stop MongoDB
```

---

## 🔄 Restart Process

### Full Restart

```powershell
# 1. Stop all
STOP_ALL.bat

# 2. Wait 5 seconds

# 3. Start all
START_ALL.bat
```

### Restart Only Backend

```powershell
# In backend terminal
Ctrl+C
node server.js
```

### Restart Only Surveillance

**Via API**:
```powershell
# Stop
curl -X POST http://localhost:3000/api/surveillance/stop -H "Authorization: Bearer YOUR_TOKEN"

# Start
curl -X POST http://localhost:3000/api/surveillance/start -H "Authorization: Bearer YOUR_TOKEN"
```

**Or**: Logout and login again

---

## 🐛 Troubleshooting

### Issue: "Port 3000 already in use"

**Solution**:
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Restart backend
cd backend-api
node server.js
```

### Issue: "Port 8080 already in use"

**Solution**:
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process
taskkill /PID <PID> /F

# Restart frontend
cd frontend
python -m http.server 8080
```

### Issue: "MongoDB not running"

**Solution**:
```powershell
# Start MongoDB
net start MongoDB

# If service doesn't exist, start manually
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath "C:\data\db"
```

### Issue: "Cannot connect to MongoDB"

**Solution**:
```powershell
# Check MongoDB status
sc query MongoDB

# Check connection
mongo --eval "db.adminCommand('ping')"

# Restart MongoDB
net stop MongoDB
net start MongoDB
```

### Issue: Surveillance not starting

**Solution**:
```powershell
# Check Python is installed
python --version

# Check if script exists
Test-Path ai-module/yolo_integrated_surveillance.py

# Check backend logs for errors
# Look in backend terminal for error messages

# Try manual start
cd ai-module
python yolo_integrated_surveillance.py
```

### Issue: Webcam not opening

**Solution**:
- Check browser permissions (allow camera)
- Try different browser (Chrome recommended)
- Check if another app is using webcam
- Close Zoom, Teams, etc.

---

## 📦 Dependencies Check

### Backend Dependencies

```powershell
cd backend-api
npm list
```

**Required packages**:
- express
- mongoose
- bcryptjs
- jsonwebtoken
- socket.io
- multer
- cors
- dotenv

**If missing**:
```powershell
npm install
```

### Frontend Dependencies

**No installation needed** - uses CDN for libraries

### Python Dependencies

```powershell
cd ai-module
pip list
```

**Required packages**:
- opencv-python
- face-recognition
- numpy
- requests
- ultralytics (for YOLOv8)

**If missing**:
```powershell
pip install opencv-python face-recognition numpy requests ultralytics
```

---

## 🔐 Credentials

### Dashboard Login
- **URL**: http://localhost:8080
- **Username**: ompriyanshu12@gmail.com
- **Password**: pradeep3133
- **Role**: admin

### MongoDB
- **URL**: mongodb://localhost:27017
- **Database**: person_detection

### API
- **Base URL**: http://localhost:3000
- **Auth**: JWT Token (obtained from login)

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────┐
│           MongoDB (Port 27017)              │
│         Database for all data               │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│      Backend API (Port 3000)                │
│  - REST API endpoints                       │
│  - Authentication                           │
│  - Surveillance control                     │
│  - Socket.IO for real-time                  │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│      Frontend (Port 8080)                   │
│  - Web Dashboard                            │
│  - Webcam capture                           │
│  - Real-time alerts                         │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│   Surveillance System (Python)              │
│  - YOLOv8 person detection                  │
│  - Face recognition                         │
│  - Real-time matching                       │
│  - Alert generation                         │
└─────────────────────────────────────────────┘
```

---

## 🎯 Startup Checklist

Before starting, verify:

- [ ] MongoDB installed and configured
- [ ] Node.js installed (v14+)
- [ ] Python installed (v3.8+)
- [ ] Backend dependencies installed (`npm install`)
- [ ] Python dependencies installed (`pip install ...`)
- [ ] Webcam connected
- [ ] Ports 3000 and 8080 are free
- [ ] .env file configured in backend-api

---

## 🚀 Production Deployment

### For Production Use

1. **Use PM2 for Backend**:
```powershell
npm install -g pm2
cd backend-api
pm2 start server.js --name person-detection-api
pm2 save
pm2 startup
```

2. **Use Nginx for Frontend**:
- Configure Nginx to serve frontend files
- Set up reverse proxy for backend

3. **MongoDB Security**:
- Enable authentication
- Use strong passwords
- Configure firewall rules

4. **SSL/HTTPS**:
- Get SSL certificate
- Configure HTTPS for both frontend and backend

---

## 📝 Quick Reference

### Start Commands
```powershell
# Start all (easiest)
START_ALL.bat

# Or manually
# Terminal 1: Backend
cd backend-api && node server.js

# Terminal 2: Frontend
cd frontend && python -m http.server 8080
```

### Stop Commands
```powershell
# Stop all
STOP_ALL.bat

# Or manually
Ctrl+C in each terminal
```

### URLs
- **Dashboard**: http://localhost:8080
- **API**: http://localhost:3000
- **API Health**: http://localhost:3000/health

### Credentials
- **Username**: ompriyanshu12@gmail.com
- **Password**: pradeep3133

---

## ✅ Success Indicators

**Everything is working when**:

1. ✅ MongoDB shows "RUNNING"
2. ✅ Backend shows "Server running on port 3000"
3. ✅ Frontend accessible at http://localhost:8080
4. ✅ Can login to dashboard
5. ✅ Surveillance starts automatically
6. ✅ Can add person with webcam
7. ✅ Detections appear in dashboard

---

## 🎉 You're Ready!

**To start everything**:
```
Double-click: START_ALL.bat
```

**Then**:
1. Browser opens automatically
2. Login with credentials
3. Surveillance starts automatically
4. Add persons with webcam
5. System detects and alerts automatically

**Everything works automatically!** 🚀

---

**Created**: October 12, 2025  
**Status**: Production Ready  
**All Features**: Integrated and Working
