# Missing Person Detection System

An AI-powered person detection and identification system using YOLOv8 for person detection and face recognition technology for matching missing persons in real-time from multiple camera feeds.

## 🌟 Features

- **Real-time Person Detection**: Uses YOLOv8 for accurate person detection from camera feeds
- **Face Recognition**: Advanced face encoding and matching with configurable similarity thresholds
- **Multi-Camera Support**: Monitor multiple camera feeds simultaneously (IP cameras & webcams)
- **Web Dashboard**: Modern web interface for managing persons, cameras, and viewing alerts
- **Real-time Alerts**: Instant notifications when a missing person is detected
- **Database Management**: Store and manage person profiles with face encodings
- **Camera Management**: Add, configure, and monitor multiple camera sources
- **Match Reports**: Track and review all detection matches with timestamps and locations
- **Priority System**: Categorize missing persons by priority (Low, Medium, High, Critical)

## 🏗️ System Architecture

```
├── frontend/              # Web dashboard (HTML/CSS/JavaScript)
├── frontend-react/        # React-based frontend (in development)
├── backend-api/           # Node.js REST API server
├── ai-module/             # Python surveillance & face recognition module
├── camera-module/         # Camera service management
├── yolov8-person-detector/ # YOLOv8 person detection module
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher)
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/priyanshulink/Missing-Person-Detection-System.git
cd Missing-Person-Detection-System
```

2. **Install Backend Dependencies**
```bash
cd backend-api
npm install
```

3. **Install Python Dependencies**
```bash
cd ../ai-module
pip install -r requirements.txt

cd ../yolov8-person-detector
pip install -r requirements.txt
```

4. **Configure Environment**

Create `.env` file in `backend-api/`:
```env
MONGODB_URI=mongodb://localhost:27017/person-detection
JWT_SECRET=your-secret-key-here
PORT=3000
```

5. **Start MongoDB**
```bash
mongod
```

6. **Seed Initial Data** (Optional)
```bash
cd backend-api
node seed-cameras.js
node update-admin.js
```

### Running the Application

#### Option 1: Start All Services (Windows)
```bash
START_ALL.bat
```

#### Option 2: Manual Start

**Terminal 1 - Backend API:**
```bash
cd backend-api
node server.js
```

**Terminal 2 - AI Surveillance:**
```bash
cd ai-module
python multi_camera_surveillance.py
```

**Terminal 3 - Frontend:**
Open `frontend/index.html` in your browser or use a local server:
```bash
cd frontend
python -m http.server 8080
```

Access the dashboard at: `http://localhost:8080`

## 📖 Usage Guide

### 1. Login
- Default credentials: `ompriyanshu12@gmail.com` / `pradeep3133`
- Access the web dashboard

### 2. Add Missing Person
- Navigate to "Persons" tab
- Click "Add Person"
- Fill in details (name, age, gender, status, priority)
- Upload photo or capture from webcam
- System automatically extracts face encoding

### 3. Configure Cameras
- Go to "Cameras" tab
- Click "Add Camera"
- Enter camera name and stream URL
- Supported formats:
  - IP Camera: `http://192.168.1.100:8080/video`
  - RTSP: `rtsp://username:password@ip:port/stream`
  - Local Webcam: `0` (device index)

### 4. Start Surveillance
- System automatically monitors all active cameras
- Detects persons using YOLOv8
- Matches faces against database
- Generates alerts when matches found (>60% similarity)

### 5. View Alerts & Reports
- Real-time alerts appear in "Alerts" tab
- Detailed match reports in "Reports" tab
- Dashboard shows statistics and recent matches

## 🎯 Key Technologies

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Socket.IO
- **Backend**: Node.js, Express.js, MongoDB, Mongoose
- **AI/ML**: 
  - YOLOv8 (Ultralytics) - Person Detection
  - face_recognition (dlib) - Face Encoding & Matching
  - OpenCV - Image Processing
- **Real-time Communication**: Socket.IO
- **Authentication**: JWT (JSON Web Tokens)

## 📁 Project Structure

```
Missing-Person-Detection-System/
│
├── frontend/                    # Web Dashboard
│   ├── index.html              # Main HTML file
│   ├── css/styles.css          # Styling
│   └── js/                     # JavaScript modules
│       ├── app.js              # Main application
│       ├── auth.js             # Authentication
│       ├── dashboard.js        # Dashboard logic
│       ├── persons.js          # Person management
│       ├── cameras.js          # Camera management
│       └── alerts.js           # Alert handling
│
├── backend-api/                 # REST API Server
│   ├── server.js               # Express server
│   ├── models/                 # MongoDB models
│   │   ├── Person.js
│   │   ├── Camera.js
│   │   ├── Report.js
│   │   └── User.js
│   ├── routes/                 # API routes
│   │   ├── auth.js
│   │   ├── persons.js
│   │   ├── cameras.js
│   │   ├── reports.js
│   │   └── upload.js
│   ├── middleware/             # Express middleware
│   └── utils/                  # Utility functions
│
├── ai-module/                   # AI Surveillance System
│   ├── multi_camera_surveillance.py  # Main surveillance
│   ├── integrated_system.py    # Integrated detection
│   ├── auto_surveillance.py    # Auto surveillance
│   └── requirements.txt        # Python dependencies
│
├── yolov8-person-detector/      # YOLOv8 Detection Module
│   ├── main.py                 # Main detector
│   ├── person_detector.py      # Detection logic
│   ├── face_matcher.py         # Face matching
│   ├── alert_system.py         # Alert generation
│   └── database/               # Person database
│
├── camera-module/               # Camera Service
│   └── camera_service.py       # Camera handling
│
├── docs/                        # Documentation
│   ├── API.md                  # API documentation
│   ├── INSTALLATION.md         # Installation guide
│   └── USAGE.md                # Usage guide
│
└── scripts/                     # Utility scripts
    ├── START_ALL.bat           # Start all services
    └── STOP_ALL.bat            # Stop all services
```

## 🔧 Configuration

### Face Recognition Settings
- **Similarity Threshold**: 60% (adjustable in code)
- **Face Encoding**: 128-dimensional vectors
- **Detection Model**: HOG (fast) or CNN (accurate)

### Camera Settings
- **Frame Processing**: Every 2nd frame (configurable)
- **Resolution**: Auto-detected from camera
- **Supported Formats**: MJPEG, RTSP, H.264

### Alert Settings
- **Real-time Alerts**: Socket.IO events
- **Alert Priority**: Based on person priority
- **Notification**: Web dashboard + console logs

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register user
- `GET /api/auth/me` - Get current user

### Persons
- `GET /api/persons` - Get all persons
- `GET /api/persons/:id` - Get person by ID
- `POST /api/persons` - Create person
- `PUT /api/persons/:id` - Update person
- `DELETE /api/persons/:id` - Delete person

### Cameras
- `GET /api/cameras` - Get all cameras
- `POST /api/cameras` - Add camera
- `PUT /api/cameras/:id` - Update camera
- `DELETE /api/cameras/:id` - Delete camera

### Reports
- `GET /api/reports` - Get all reports
- `GET /api/reports/:id` - Get report by ID

See [API Documentation](docs/API.md) for detailed information.

## 🧪 Testing

### Test Camera Connection
```bash
python test_camera_stream.py
```

### Test Face Encoding
```bash
python test-face-encoding.py <image_path>
```

### Test Live Detection
```bash
python test-live-detection.py
```

### Test All Cameras
```bash
python test_all_cameras.py
```

## 🐛 Troubleshooting

### Camera Not Connecting
- Verify camera URL is correct
- Check network connectivity
- Ensure camera is on same network
- Test URL in browser first

### Face Recognition Not Working
- Ensure clear, front-facing photos
- Good lighting conditions
- Face should be visible and unobstructed
- Photo resolution should be reasonable

### MongoDB Connection Issues
- Verify MongoDB is running
- Check connection string in `.env`
- Ensure database permissions

### Performance Issues
- Reduce frame processing rate
- Lower camera resolution
- Use GPU acceleration (if available)
- Monitor system resources

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Priyanshu Singh** - [priyanshulink](https://github.com/priyanshulink)

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- face_recognition library by Adam Geitgey
- OpenCV community
- MongoDB team

## 📧 Contact

For questions or support, please open an issue on GitHub or contact:
- Email: ompriyanshu12@gmail.com
- GitHub: [@priyanshulink](https://github.com/priyanshulink)

## 🔗 Links

- [Project Repository](https://github.com/priyanshulink/Missing-Person-Detection-System)
- [Documentation](docs/)
- [Issue Tracker](https://github.com/priyanshulink/Missing-Person-Detection-System/issues)

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
