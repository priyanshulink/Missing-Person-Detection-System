"""
Configuration file for YOLOv8 Person Detection System
"""

# Camera Settings
CAMERA_INDEX = 0  # Default camera (0 for built-in webcam, 1+ for external cameras)
CAMERA_NAME = 'Main Entrance Camera'  # Name of the camera
CAMERA_LOCATION = 'Building A - Main Entrance'  # Physical location of the camera
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

# YOLOv8 Settings
YOLO_MODEL = 'yolov8n.pt'  # Options: yolov8n (fastest), yolov8s, yolov8m, yolov8l, yolov8x (most accurate)
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for person detection (0.0 - 1.0)

# Face Recognition Settings
FACE_MATCH_TOLERANCE = 0.6  # Lower is stricter (0.0 - 1.0, recommended: 0.4 - 0.6)
DATABASE_PATH = 'database/persons'
API_URL = 'http://localhost:5000'  # Backend API URL for loading missing persons
AUTO_RELOAD_INTERVAL = 30  # Seconds between automatic database reloads (0 = disabled)

# Alert Settings
ALERT_COOLDOWN = 5  # Seconds between alerts for same person
ALERT_BANNER_DURATION = 3  # Seconds to show alert banner on screen

# Performance Settings
SKIP_FRAMES = 2  # Skip N frames between processing (2 = process every 3rd frame)
MIN_PERSON_SIZE = 60  # Minimum width/height in pixels for face matching (increased for speed)
RESIZE_FRAME_MAX = 1280  # Maximum frame width for processing

# Display Settings
SHOW_FPS = True
SHOW_INFO_PANEL = True
WINDOW_NAME = 'YOLOv8 Person Detection & Recognition'
