"""
Automatic Surveillance System
Continuously monitors webcam and detects persons automatically
Runs in background and sends alerts when persons are detected
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

# Configuration
API_URL = 'http://localhost:3000'
CAMERA_ID = 'webcam_surveillance'
CONFIDENCE_THRESHOLD = 0.6
PROCESS_EVERY_N_FRAMES = 3
CHECK_DATABASE_INTERVAL = 30  # Reload persons every 30 seconds
MATCH_COOLDOWN = 10  # seconds between alerts for same person

class AutoSurveillance:
    def __init__(self):
        self.video_capture = None
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.frame_count = 0
        self.last_match_time = {}
        self.last_database_check = 0
        self.running = False
        
    def load_persons_from_api(self):
        """Load persons with face encodings from API (only missing persons)"""
        try:
            print(f"🔄 Loading missing persons from database...")
            response = requests.get(f'{API_URL}/api/persons?status=missing&limit=1000', timeout=5)
            
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
                    print("⚠️  No persons with face encodings found in database")
                    print("💡 Add persons with photos via dashboard to enable detection")
                
                self.last_database_check = time.time()
                return True
            else:
                print(f"❌ Failed to load persons: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to API at {API_URL}")
            print("💡 Make sure backend server is running")
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
            
            # Set camera properties for better performance
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.video_capture.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✅ Camera {camera_index} initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def send_detection_alert(self, person_id, person_name, similarity, face_location, frame):
        """Send detection alert to API"""
        try:
            # Check cooldown
            current_time = time.time()
            if person_id in self.last_match_time:
                if current_time - self.last_match_time[person_id] < MATCH_COOLDOWN:
                    return  # Skip if within cooldown
            
            # Prepare detection data
            data = {
                'encoding': [0] * 128,  # Dummy encoding
                'metadata': {
                    'camera_id': CAMERA_ID,
                    'timestamp': datetime.now().isoformat(),
                    'location': 'Webcam Surveillance',
                    'bbox': face_location,
                    'detection_confidence': float(similarity),
                    'person_id': person_id,
                    'person_name': person_name
                }
            }
            
            # Send to API
            response = requests.post(f'{API_URL}/api/recognize', json=data, timeout=5)
            
            if response.status_code == 200:
                print(f"🚨 ALERT: {person_name} detected! (confidence: {similarity:.2%})")
                self.last_match_time[person_id] = current_time
            else:
                print(f"⚠️  Failed to send alert: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending alert: {e}")
    
    def process_frame(self, frame):
        """Process frame for face detection and recognition"""
        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
        
        if len(face_locations) == 0:
            return [], [], []
        
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        face_similarities = []
        face_ids = []
        
        for face_encoding in face_encodings:
            name = "Unknown"
            similarity = 0.0
            person_id = None
            
            if len(self.known_face_encodings) > 0:
                # Compare with known faces
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
                        
                        # Send alert if match is good enough
                        if similarity >= CONFIDENCE_THRESHOLD:
                            face_loc = face_locations[len(face_names)]
                            self.send_detection_alert(person_id, name, similarity, {
                                'top': int(face_loc[0] * 4),
                                'right': int(face_loc[1] * 4),
                                'bottom': int(face_loc[2] * 4),
                                'left': int(face_loc[3] * 4)
                            }, frame)
            
            face_names.append(name)
            face_similarities.append(similarity)
            face_ids.append(person_id)
        
        return face_locations, face_names, face_similarities
    
    def draw_detections(self, frame, face_locations, face_names, face_similarities):
        """Draw detection boxes and labels on frame"""
        for (top, right, bottom, left), name, similarity in zip(face_locations, face_names, face_similarities):
            # Scale back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Choose color
            if name != "Unknown":
                color = (0, 255, 0)  # Green for known
                label = f"{name} ({similarity:.0%})"
            else:
                color = (0, 0, 255)  # Red for unknown
                label = "Unknown"
            
            # Draw box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw label text
            cv2.putText(frame, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Add status info
        status_text = f"Monitoring: {len(self.known_face_encodings)} persons | Frame: {self.frame_count}"
        cv2.putText(frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Main surveillance loop"""
        print("=" * 60)
        print("🎥 AUTOMATIC SURVEILLANCE SYSTEM")
        print("=" * 60)
        print(f"API URL: {API_URL}")
        print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
        print(f"Match Cooldown: {MATCH_COOLDOWN}s")
        print("=" * 60)
        
        # Load persons from database
        if not self.load_persons_from_api():
            print("\n⚠️  Warning: Could not load persons from database")
            print("System will continue but won't detect anyone until persons are loaded")
        
        # Initialize camera
        if not self.initialize_camera():
            print("\n❌ Failed to initialize camera. Exiting.")
            return
        
        print("\n✅ SURVEILLANCE ACTIVE")
        print("=" * 60)
        print("Controls:")
        print("  'q' - Quit")
        print("  'r' - Reload persons from database")
        print("  's' - Show/Hide video window")
        print("=" * 60)
        
        self.running = True
        show_window = True
        
        try:
            while self.running:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("❌ Failed to grab frame")
                    time.sleep(0.1)
                    continue
                
                # Check if we need to reload database
                if time.time() - self.last_database_check > CHECK_DATABASE_INTERVAL:
                    self.load_persons_from_api()
                
                # Process every Nth frame
                if self.frame_count % PROCESS_EVERY_N_FRAMES == 0:
                    face_locations, face_names, face_similarities = self.process_frame(frame)
                    
                    # Draw detections
                    if show_window:
                        frame = self.draw_detections(frame, face_locations, face_names, face_similarities)
                
                self.frame_count += 1
                
                # Display frame
                if show_window:
                    cv2.imshow('Surveillance Monitor', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n👋 Shutting down surveillance...")
                    break
                elif key == ord('r'):
                    print("\n🔄 Reloading persons from database...")
                    self.load_persons_from_api()
                elif key == ord('s'):
                    show_window = not show_window
                    if not show_window:
                        cv2.destroyAllWindows()
                        print("📺 Video window hidden (press 's' to show)")
                    else:
                        print("📺 Video window shown")
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error in surveillance loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.running = False
        if self.video_capture:
            self.video_capture.release()
        cv2.destroyAllWindows()
        print("✅ Surveillance stopped")


def check_backend_connection():
    """Check if backend server is running"""
    try:
        response = requests.get(f'{API_URL}/health', timeout=3)
        if response.status_code == 200:
            print(f"✅ Backend server is running at {API_URL}")
            return True
        else:
            print(f"⚠️  Backend server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to backend server at {API_URL}")
        print("💡 Please start the backend server first:")
        print("   cd backend-api")
        print("   node server.js")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False


if __name__ == '__main__':
    print("\n🚀 Starting Automatic Surveillance System...\n")
    
    # Check backend connection
    if not check_backend_connection():
        print("\n❌ Cannot start surveillance without backend server")
        sys.exit(1)
    
    # Start surveillance
    surveillance = AutoSurveillance()
    surveillance.run()
    
    print("\n✅ Surveillance system terminated")
