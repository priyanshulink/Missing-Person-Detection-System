# Installation Guide

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux, or macOS
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 5GB free space
- **GPU**: NVIDIA GPU with CUDA support (optional, for better performance)

### Software Requirements

#### Python Environment
- Python 3.8 or higher
- pip package manager

#### Node.js Environment
- Node.js 16.x or higher
- npm package manager

#### Database
- MongoDB 5.0 or higher

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
cd c:/Users/91900/Downloads/project
```

### 2. Install MongoDB

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Choose "Complete" installation
4. Install MongoDB as a service
5. Verify installation:
```powershell
mongod --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 3. Setup Camera Module

```bash
cd camera-module
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

**Note**: Installing `dlib` on Windows may require Visual Studio Build Tools.

### 4. Setup AI/ML Module

```bash
cd ../ai-module
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

**Download YOLOv8 Model**:
The first time you run the AI module, it will automatically download the YOLOv8 model (~6MB).

### 5. Setup Backend API

```bash
cd ../backend-api
npm install
```

**Configure Environment Variables**:
```bash
cp .env.example .env
```

Edit `.env` file and update:
```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/person_detection
JWT_SECRET=your_secure_random_string_here
```

**Firebase Setup (Optional)**:
1. Create a Firebase project at [console.firebase.google.com](https://console.firebase.google.com)
2. Generate a service account key
3. Save as `firebase-credentials.json` in `backend-api/` directory
4. Update `FIREBASE_CREDENTIALS_PATH` in `.env`

### 6. Setup Frontend

The frontend is a static HTML/CSS/JS application. No build step required.

**Configure API URL**:
Edit `frontend/js/config.js`:
```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:3000',
    SOCKET_URL: 'http://localhost:3000'
};
```

## Verification

### Test MongoDB Connection
```bash
mongosh
# or
mongo
```

### Test Python Environment
```bash
cd camera-module
python -c "import cv2; print('OpenCV:', cv2.__version__)"
```

### Test Node.js Backend
```bash
cd backend-api
npm start
```
Visit: http://localhost:3000/health

### Test Frontend
Open `frontend/index.html` in a web browser or use a local server:
```bash
cd frontend
python -m http.server 8080
```
Visit: http://localhost:8080

## Common Issues

### Issue: dlib installation fails on Windows
**Solution**: Install Visual Studio Build Tools
```bash
# Download from: https://visualstudio.microsoft.com/downloads/
# Install "Desktop development with C++"
```

### Issue: MongoDB connection refused
**Solution**: Ensure MongoDB service is running
```powershell
# Windows
net start MongoDB

# Linux
sudo systemctl start mongodb
```

### Issue: Camera not detected
**Solution**: 
- Check camera permissions
- Update camera index in `camera-module/config.json`
- Try different camera sources (0, 1, 2, etc.)

### Issue: CUDA/GPU errors
**Solution**: 
- Install CUDA toolkit and cuDNN
- Or use CPU-only mode (slower but works)
- Update PyTorch installation for your system

## Next Steps

After installation, proceed to [USAGE.md](./USAGE.md) for instructions on running the system.
