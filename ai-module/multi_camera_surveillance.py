"""
Multi-Camera Surveillance System
Processes multiple camera streams simultaneously using threading
"""

import cv2
import face_recognition
import numpy as np
import requests
import json
import threading
import time
from datetime import datetime
from pathlib import Path
import sys

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
BACKEND_URL = 'http://localhost:3000'
YOLO_MODEL_PATH = str(yolo_path / 'yolov8n.pt')
YOLO_CONFIDENCE = 0.5
FACE_CONFIDENCE_THRESHOLD = 0.4  # Minimum confidence for face detection
FACE_MATCH_THRESHOLD = 0.45  # Alert only if 55% or above similarity (distance 0.45 = 55% match)
PROCESS_EVERY_N_FRAMES = 3  # Increased from 2 to 3 for better performance
MATCH_COOLDOWN = 10  # seconds between alerts for same person on same camera
CHECK_DATABASE_INTERVAL = 10  # seconds - check for new cameras
RESIZE_FRAME_WIDTH = 640  # Resize frames for faster processing

class CameraProcessor:
    """Processes a single camera stream"""
    
    def __init__(self, camera_config, yolo_model=None):
        self.camera_id = camera_config['cameraId']
        self.camera_name = camera_config['name']
        self.location = camera_config['location']
        self.stream_url = camera_config['streamUrl']
        self.yolo_model = yolo_model
        
        self.video_capture = None
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.frame_count = 0
        self.last_match_time = {}
        self.last_database_check = 0
        self.running = False
        self.thread = None
        
        print(f"📹 Initialized camera: {self.camera_name} ({self.camera_id})")
    
    def load_persons_from_api(self):
        """Load persons with face encodings from API (only missing persons)"""
        try:
            # Only load persons with status=missing
            response = requests.get(f'{BACKEND_URL}/api/persons?status=missing&limit=1000', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                persons = data.get('persons', [])
                
                self.known_face_encodings = []
                self.known_face_names = []
                self.known_face_ids = []
                
                for person in persons:
                    if person.get('faceEncodings') and len(person['faceEncodings']) > 0:
                        for enc_data in person['faceEncodings']:
                            encoding = enc_data.get('encoding')
                            if encoding and len(encoding) == 128:
                                self.known_face_encodings.append(np.array(encoding))
                                self.known_face_names.append(person.get('name', 'Unknown'))
                                self.known_face_ids.append(str(person.get('_id', '')))
                
                print(f"[{self.camera_name}] ✅ Loaded {len(self.known_face_encodings)} face encodings")
                return True
            else:
                print(f"[{self.camera_name}] ⚠️  Failed to load persons: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[{self.camera_name}] ❌ Error loading persons: {e}")
            return False
    
    def detect_persons_yolo(self, frame):
        """Detect persons using YOLOv8"""
        if not self.yolo_model:
            return []
        
        try:
            results = self.yolo_model(frame, verbose=False)
            detections = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # Class 0 is 'person' in COCO dataset
                    if class_id == 0 and confidence >= YOLO_CONFIDENCE:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        detections.append({
                            'bbox': (x1, y1, x2, y2),
                            'confidence': confidence
                        })
            
            return detections
        except Exception as e:
            print(f"[{self.camera_name}] ⚠️  YOLO detection error: {e}")
            return []
    
    def match_face(self, face_image):
        """Match face against known encodings"""
        if len(self.known_face_encodings) == 0:
            return None, None, 0, None
        
        try:
            # Convert to RGB
            rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            
            # Resize for faster face detection
            height, width = rgb_face.shape[:2]
            if width > 400:
                scale = 400 / width
                new_width = 400
                new_height = int(height * scale)
                rgb_face = cv2.resize(rgb_face, (new_width, new_height))
            
            # Get face encodings with faster HOG model
            face_locations = face_recognition.face_locations(rgb_face, model='hog', number_of_times_to_upsample=0)
            
            if not face_locations:
                return None, None, 0, None
            
            face_encodings = face_recognition.face_encodings(rgb_face, face_locations, num_jitters=1)
            
            if not face_encodings:
                return None, None, 0, None
            
            face_encoding = face_encodings[0]
            
            # Calculate distances
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            # Find best match
            best_match_index = np.argmin(face_distances)
            best_distance = face_distances[best_match_index]
            
            # Check threshold - Alert only if 55% or above similarity
            if best_distance <= FACE_MATCH_THRESHOLD:  # 0.45 distance = 55% similarity minimum
                similarity = 1 - best_distance
                return (
                    self.known_face_names[best_match_index],
                    self.known_face_ids[best_match_index],
                    similarity,
                    face_encoding  # Return the actual face encoding
                )
            
            return None, None, 0, None
            
        except Exception as e:
            print(f"[{self.camera_name}] ⚠️  Face matching error: {e}")
            return None, None, 0, None
    
    def send_match_to_backend(self, person_name, person_id, similarity, bbox, face_encoding):
        """Send match detection to backend"""
        try:
            current_time = time.time()
            
            # Check cooldown
            if person_id in self.last_match_time:
                if current_time - self.last_match_time[person_id] < MATCH_COOLDOWN:
                    return
            
            # Prepare payload with real face encoding
            payload = {
                'encoding': face_encoding.tolist() if face_encoding is not None else [0] * 128,
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
            
            response = requests.post(f'{BACKEND_URL}/api/recognition', json=payload, timeout=5)
            
            if response.status_code == 200:
                self.last_match_time[person_id] = current_time
                print(f"[{self.camera_name}] 🚨 ALERT: {person_name} detected (similarity: {similarity:.2%})")
            else:
                print(f"[{self.camera_name}] ⚠️  Backend response: {response.status_code}")
                
        except Exception as e:
            print(f"[{self.camera_name}] ❌ Error sending to backend: {e}")
    
    def update_camera_status(self):
        """Update camera status in backend"""
        try:
            requests.patch(
                f'{BACKEND_URL}/api/cameras/{self.camera_id}/status',
                json={'status': 'active', 'lastOnline': datetime.now().isoformat()},
                timeout=5
            )
        except:
            pass
    
    def process_stream(self):
        """Main processing loop for this camera"""
        print(f"[{self.camera_name}] 🎥 Starting stream processing...")
        
        # Open video capture
        self.video_capture = cv2.VideoCapture(self.stream_url)
        
        if not self.video_capture.isOpened():
            print(f"[{self.camera_name}] ❌ Failed to open stream: {self.stream_url}")
            return
        
        # Load initial person database
        self.load_persons_from_api()
        
        self.running = True
        
        while self.running:
            ret, frame = self.video_capture.read()
            
            if not ret:
                print(f"[{self.camera_name}] ⚠️  Failed to read frame, retrying...")
                time.sleep(1)
                continue
            
            self.frame_count += 1
            
            # Reload database periodically
            current_time = time.time()
            if current_time - self.last_database_check > CHECK_DATABASE_INTERVAL:
                self.load_persons_from_api()
                self.last_database_check = current_time
                self.update_camera_status()
            
            # Process every Nth frame
            if self.frame_count % PROCESS_EVERY_N_FRAMES != 0:
                continue
            
            # Resize frame for faster processing
            height, width = frame.shape[:2]
            if width > RESIZE_FRAME_WIDTH:
                scale = RESIZE_FRAME_WIDTH / width
                new_width = RESIZE_FRAME_WIDTH
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Detect persons
            if YOLO_AVAILABLE and self.yolo_model:
                detections = self.detect_persons_yolo(frame)
            else:
                # Fallback: treat whole frame as detection
                h, w = frame.shape[:2]
                detections = [{'bbox': (0, 0, w, h), 'confidence': 1.0}]
            
            # Process each detection
            for detection in detections:
                x1, y1, x2, y2 = detection['bbox']
                
                # Crop person region
                person_crop = frame[y1:y2, x1:x2]
                
                if person_crop.shape[0] < 50 or person_crop.shape[1] < 50:
                    continue
                
                # Match face
                person_name, person_id, similarity, face_encoding = self.match_face(person_crop)
                
                if person_name and similarity >= FACE_CONFIDENCE_THRESHOLD:
                    self.send_match_to_backend(person_name, person_id, similarity, (x1, y1, x2, y2), face_encoding)
        
        # Cleanup
        if self.video_capture:
            self.video_capture.release()
        
        print(f"[{self.camera_name}] 🛑 Stream processing stopped")
    
    def start(self):
        """Start processing in a separate thread"""
        if not self.running:
            self.thread = threading.Thread(target=self.process_stream, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop processing"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)


class MultiCameraSurveillance:
    """Manages multiple camera processors"""
    
    def __init__(self):
        self.cameras = []
        self.processors = []
        self.yolo_model = None
    
    def initialize_yolo(self):
        """Initialize YOLO model (shared across cameras)"""
        if not YOLO_AVAILABLE:
            print("⚠️  YOLOv8 not available")
            return False
        
        try:
            print("🔄 Loading YOLOv8 model...")
            self.yolo_model = YOLO(YOLO_MODEL_PATH)
            print("✅ YOLOv8 model loaded")
            return True
        except Exception as e:
            print(f"❌ Error loading YOLO: {e}")
            return False
    
    def load_cameras_from_api(self):
        """Load camera configurations from backend"""
        try:
            print("🔄 Loading camera configurations...")
            response = requests.get(f'{BACKEND_URL}/api/cameras/active/list', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                all_cameras = data.get('cameras', [])
                
                # Filter out local webcam (streamUrl = "0" or contains "cam_local")
                self.cameras = [
                    cam for cam in all_cameras 
                    if cam.get('streamUrl') != '0' and 
                       cam.get('streamUrl') != 0 and
                       'cam_local' not in cam.get('cameraId', '').lower()
                ]
                
                skipped = len(all_cameras) - len(self.cameras)
                if skipped > 0:
                    print(f"⚠️  Skipped {skipped} local webcam(s)")
                
                print(f"✅ Loaded {len(self.cameras)} network cameras")
                return True
            else:
                print(f"⚠️  Failed to load cameras: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading cameras: {e}")
            return False
    
    def start_all_cameras(self):
        """Start processing all cameras"""
        if not self.cameras:
            print("❌ No cameras configured")
            return
        
        print(f"\n🚀 Starting surveillance on {len(self.cameras)} cameras...\n")
        
        for camera_config in self.cameras:
            processor = CameraProcessor(camera_config, self.yolo_model)
            processor.start()
            self.processors.append(processor)
            time.sleep(0.5)  # Stagger starts
        
        print("\n✅ All cameras started\n")
    
    def stop_all_cameras(self):
        """Stop all camera processors"""
        print("\n🛑 Stopping all cameras...")
        
        for processor in self.processors:
            processor.stop()
        
        self.processors = []
        print("✅ All cameras stopped\n")
    
    def reload_cameras(self):
        """Reload cameras from API and start any new ones"""
        print("\n🔄 Checking for new cameras...")
        
        # Get current camera IDs
        current_camera_ids = set(p.camera_id for p in self.processors)
        
        # Load cameras from API
        try:
            response = requests.get(f'{BACKEND_URL}/api/cameras/active/list', timeout=10)
            if response.status_code == 200:
                data = response.json()
                new_cameras = data.get('cameras', [])
                new_camera_ids = set(cam['cameraId'] for cam in new_cameras)
                
                # Find cameras that need to be added
                cameras_to_add = [cam for cam in new_cameras if cam['cameraId'] not in current_camera_ids]
                
                # Find cameras that need to be removed
                cameras_to_remove = [p for p in self.processors if p.camera_id not in new_camera_ids]
                
                # Remove old cameras
                for processor in cameras_to_remove:
                    print(f"🛑 Stopping removed camera: {processor.camera_name}")
                    processor.stop()
                    self.processors.remove(processor)
                
                # Add new cameras
                if cameras_to_add:
                    print(f"✅ Found {len(cameras_to_add)} new camera(s)")
                    for camera_config in cameras_to_add:
                        processor = CameraProcessor(camera_config, self.yolo_model)
                        processor.start()
                        self.processors.append(processor)
                        time.sleep(0.5)
                else:
                    print("ℹ️  No new cameras")
                    
        except Exception as e:
            print(f"⚠️  Error reloading cameras: {e}")
    
    def run(self):
        """Main run loop"""
        print("="*60)
        print("Multi-Camera Surveillance System")
        print("="*60)
        
        # Initialize YOLO
        self.initialize_yolo()
        
        # Load cameras
        if not self.load_cameras_from_api():
            print("⚠️  No cameras configured initially. Will check periodically...")
        else:
            # Start all cameras
            self.start_all_cameras()
        
        # Keep running and check for new cameras periodically
        last_reload = time.time()
        reload_interval = CHECK_DATABASE_INTERVAL
        
        try:
            print("Press Ctrl+C to stop\n")
            print(f"ℹ️  Will check for new cameras every {reload_interval} seconds\n")
            
            while True:
                time.sleep(1)
                
                # Check if it's time to reload cameras
                if time.time() - last_reload >= reload_interval:
                    self.reload_cameras()
                    last_reload = time.time()
                    
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
        finally:
            self.stop_all_cameras()


if __name__ == "__main__":
    surveillance = MultiCameraSurveillance()
    surveillance.run()
