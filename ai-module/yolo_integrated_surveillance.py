"""
Integrated YOLOv8 + Face Recognition Surveillance System
Combines YOLOv8 person detection with face recognition
Automatically starts on login and integrates with dashboard
"""

import cv2
import face_recognition
import numpy as np
import requests
import json
from datetime import datetime
import time
import sys
import os
from pathlib import Path

# Add yolov8-person-detector to path
yolo_path = Path(__file__).parent.parent / 'yolov8-person-detector'
sys.path.insert(0, str(yolo_path))

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    print("⚠️  YOLOv8 not available, using basic face detection")
    YOLO_AVAILABLE = False

# Configuration
API_URL = 'http://localhost:3000'
CAMERA_ID = 'yolo_surveillance'
CAMERA_NAME = 'Main Entrance Camera'  # Name of the camera
CAMERA_LOCATION = 'Building A - Main Entrance'  # Physical location of the camera
YOLO_MODEL_PATH = str(yolo_path / 'yolov8n.pt')
CONFIDENCE_THRESHOLD = 0.40  # Lowered for better detection (was 0.45)
YOLO_CONFIDENCE = 0.5
PROCESS_EVERY_N_FRAMES = 2
CHECK_DATABASE_INTERVAL = 30
MATCH_COOLDOWN = 10

class YOLOIntegratedSurveillance:
    def __init__(self):
        self.video_capture = None
        self.yolo_model = None
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.frame_count = 0
        self.last_match_time = {}
        self.last_database_check = 0
        self.running = False
        
    def initialize_yolo(self):
        """Initialize YOLOv8 model"""
        if not YOLO_AVAILABLE:
            print("⚠️  YOLOv8 not available, skipping YOLO initialization")
            return False
            
        try:
            if not os.path.exists(YOLO_MODEL_PATH):
                print(f"⚠️  YOLO model not found at {YOLO_MODEL_PATH}")
                return False
                
            print("🔄 Loading YOLOv8 model...")
            self.yolo_model = YOLO(YOLO_MODEL_PATH)
            print("✅ YOLOv8 model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            return False
    
    def load_persons_from_api(self):
        """Load persons with face encodings from API (only missing persons)"""
        try:
            print(f"🔄 Loading missing persons from database...")
            # Only load persons with status=missing
            response = requests.get(f'{API_URL}/api/persons?status=missing&limit=1000', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                persons = data.get('persons', [])
                
                self.known_face_encodings = []
                self.known_face_names = []
                self.known_face_ids = []
                
                for person in persons:
                    if person.get('faceEncodings') and len(person['faceEncodings']) > 0:
                        for encoding_data in person['faceEncodings']:
                            encoding = encoding_data.get('encoding')
                            if encoding and len(encoding) == 128:
                                self.known_face_encodings.append(np.array(encoding))
                                self.known_face_names.append(person['name'])
                                self.known_face_ids.append(str(person['_id']))
                
                print(f"✅ Loaded {len(self.known_face_encodings)} face encodings from {len(persons)} persons")
                
                if len(self.known_face_encodings) == 0:
                    print("⚠️  No persons with face encodings found")
                    print("💡 Add persons with photos via dashboard")
                
                self.last_database_check = time.time()
                return True
            else:
                print(f"❌ Failed to load persons: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading persons: {e}")
            return False
    
    def initialize_camera(self, camera_index=0):
        """Initialize webcam"""
        try:
            self.video_capture = cv2.VideoCapture(camera_index)
            
            if not self.video_capture.isOpened():
                print(f"❌ Could not open camera {camera_index}")
                return False
            
            # Set camera properties
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.video_capture.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✅ Camera {camera_index} initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def detect_persons_yolo(self, frame):
        """Detect persons using YOLOv8"""
        if not self.yolo_model:
            return []
        
        try:
            results = self.yolo_model(frame, conf=YOLO_CONFIDENCE, classes=[0], verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    
                    # Crop person region
                    cropped = frame[y1:y2, x1:x2]
                    
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': conf,
                        'cropped': cropped
                    })
            
            return detections
        except Exception as e:
            print(f"❌ YOLO detection error: {e}")
            return []
    
    def detect_faces_in_person(self, person_image):
        """Detect and match faces in person crop"""
        try:
            # Resize if too large
            if person_image.shape[0] > 500:
                scale = 500 / person_image.shape[0]
                person_image = cv2.resize(person_image, None, fx=scale, fy=scale)
            
            rgb_image = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)
            
            # Find faces
            face_locations = face_recognition.face_locations(rgb_image, model='hog')
            
            if len(face_locations) == 0:
                return None, 0.0, None
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            if len(face_encodings) == 0:
                return None, 0.0, None
            
            # Match against known faces
            face_encoding = face_encodings[0]
            
            if len(self.known_face_encodings) == 0:
                return None, 0.0, None
            
            matches = face_recognition.compare_faces(
                self.known_face_encodings,
                face_encoding,
                tolerance=CONFIDENCE_THRESHOLD
            )
            
            face_distances = face_recognition.face_distance(
                self.known_face_encodings,
                face_encoding
            )
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    person_id = self.known_face_ids[best_match_index]
                    similarity = 1.0 - face_distances[best_match_index]
                    
                    return name, similarity, person_id
            
            return None, 0.0, None
            
        except Exception as e:
            print(f"❌ Face detection error: {e}")
            return None, 0.0, None
    
    def send_detection_alert(self, person_id, person_name, similarity, bbox):
        """Send detection alert to API"""
        try:
            current_time = time.time()
            if person_id in self.last_match_time:
                if current_time - self.last_match_time[person_id] < MATCH_COOLDOWN:
                    return
            
            data = {
                'encoding': [0] * 128,
                'metadata': {
                    'camera_id': CAMERA_ID,
                    'camera_name': CAMERA_NAME,
                    'camera_location': CAMERA_LOCATION,
                    'timestamp': datetime.now().isoformat(),
                    'location': 'YOLO Surveillance',
                    'bbox': {'x1': bbox[0], 'y1': bbox[1], 'x2': bbox[2], 'y2': bbox[3]},
                    'detection_confidence': float(similarity),
                    'person_id': person_id,
                    'person_name': person_name
                }
            }
            
            response = requests.post(f'{API_URL}/api/recognize', json=data, timeout=5)
            
            if response.status_code == 200:
                print(f"🚨 ALERT: {person_name} detected! (confidence: {similarity:.2%})")
                self.last_match_time[person_id] = current_time
            
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
    
    def draw_detections(self, frame, detections, matches):
        """Draw bounding boxes and labels"""
        for detection, match in zip(detections, matches):
            x1, y1, x2, y2 = detection['bbox']
            yolo_conf = detection['confidence']
            
            name, similarity, person_id = match
            
            if name:
                color = (0, 255, 0)  # Green for known
                label = f"{name} ({similarity:.0%})"
            else:
                color = (0, 0, 255)  # Red for unknown
                label = f"Person ({yolo_conf:.0%})"
            
            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (x1, y2 - label_size[1] - 10), 
                         (x1 + label_size[0], y2), color, cv2.FILLED)
            
            # Draw label text
            cv2.putText(frame, label, (x1, y2 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add status info
        status = f"YOLOv8 + Face Recognition | Monitoring: {len(self.known_face_encodings)} persons"
        cv2.putText(frame, status, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Main surveillance loop"""
        print("=" * 70)
        print("🎥 YOLO INTEGRATED SURVEILLANCE SYSTEM")
        print("=" * 70)
        print(f"API URL: {API_URL}")
        print(f"YOLO Model: {YOLO_MODEL_PATH}")
        print(f"Face Confidence: {CONFIDENCE_THRESHOLD}")
        print("=" * 70)
        
        # Initialize YOLO
        yolo_enabled = self.initialize_yolo()
        if not yolo_enabled:
            print("⚠️  Running without YOLO (face detection only)")
        
        # Load persons
        if not self.load_persons_from_api():
            print("⚠️  Could not load persons from database")
        
        # Initialize camera
        if not self.initialize_camera():
            print("❌ Failed to initialize camera. Exiting.")
            return
        
        print("\n✅ SURVEILLANCE ACTIVE")
        print("=" * 70)
        print("Controls: 'q' - Quit | 'r' - Reload | 's' - Show/Hide")
        print("=" * 70)
        
        self.running = True
        show_window = True
        fps_start = time.time()
        fps_counter = 0
        fps = 0
        
        try:
            while self.running:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("❌ Failed to grab frame")
                    time.sleep(0.1)
                    continue
                
                # Check database reload
                if time.time() - self.last_database_check > CHECK_DATABASE_INTERVAL:
                    self.load_persons_from_api()
                
                # Process frame
                if self.frame_count % PROCESS_EVERY_N_FRAMES == 0:
                    if yolo_enabled:
                        # Use YOLO for person detection
                        detections = self.detect_persons_yolo(frame)
                        
                        # Match faces in detected persons
                        matches = []
                        for detection in detections:
                            name, similarity, person_id = self.detect_faces_in_person(detection['cropped'])
                            matches.append((name, similarity, person_id))
                            
                            # Send alert if matched
                            if name and similarity >= CONFIDENCE_THRESHOLD:
                                self.send_detection_alert(person_id, name, similarity, detection['bbox'])
                        
                        # Draw detections
                        if show_window:
                            frame = self.draw_detections(frame, detections, matches)
                    else:
                        # Fallback to basic face detection
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(rgb_small)
                        
                        if show_window and len(face_locations) > 0:
                            for (top, right, bottom, left) in face_locations:
                                top, right, bottom, left = top*4, right*4, bottom*4, left*4
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                self.frame_count += 1
                
                # Calculate FPS
                fps_counter += 1
                if fps_counter >= 30:
                    fps = fps_counter / (time.time() - fps_start)
                    fps_start = time.time()
                    fps_counter = 0
                
                # Display
                if show_window:
                    cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.imshow('YOLO Surveillance', frame)
                
                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n👋 Shutting down...")
                    break
                elif key == ord('r'):
                    print("\n🔄 Reloading persons...")
                    self.load_persons_from_api()
                elif key == ord('s'):
                    show_window = not show_window
                    if not show_window:
                        cv2.destroyAllWindows()
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.running = False
        if self.video_capture:
            self.video_capture.release()
        cv2.destroyAllWindows()
        print("✅ Surveillance stopped")


def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f'{API_URL}/health', timeout=3)
        if response.status_code == 200:
            print(f"✅ Backend server running at {API_URL}")
            return True
    except:
        print(f"❌ Cannot connect to backend at {API_URL}")
        print("💡 Start backend: cd backend-api && node server.js")
        return False


if __name__ == '__main__':
    print("\n🚀 Starting YOLO Integrated Surveillance...\n")
    
    if not check_backend():
        sys.exit(1)
    
    surveillance = YOLOIntegratedSurveillance()
    surveillance.run()
    
    print("\n✅ System terminated")
