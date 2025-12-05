"""
Webcam Face Detection and Recognition
Real-time face detection and matching using webcam
"""

import cv2
import face_recognition
import numpy as np
import requests
import json
from datetime import datetime
import time

# Configuration
API_URL = 'http://localhost:3000'
CAMERA_ID = 'webcam_0'
CONFIDENCE_THRESHOLD = 0.6
PROCESS_EVERY_N_FRAMES = 5  # Process every 5th frame for better performance

class WebcamDetection:
    def __init__(self):
        self.video_capture = None
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.frame_count = 0
        self.last_match_time = {}
        self.match_cooldown = 10  # seconds between matches for same person
        
    def load_known_faces(self):
        """Load known faces from API (only missing persons)"""
        try:
            response = requests.get(f'{API_URL}/api/persons?status=missing&limit=1000')
            if response.status_code == 200:
                data = response.json()
                persons = data.get('persons', [])
                
                self.known_face_encodings = []
                self.known_face_names = []
                self.known_face_ids = []
                
                for person in persons:
                    if person.get('faceEncodings'):
                        for encoding_data in person['faceEncodings']:
                            encoding = encoding_data.get('encoding')
                            if encoding and len(encoding) == 128:
                                self.known_face_encodings.append(np.array(encoding))
                                self.known_face_names.append(person['name'])
                                self.known_face_ids.append(str(person['_id']))
                
                print(f"✅ Loaded {len(self.known_face_encodings)} face encodings from {len(persons)} persons")
                return True
            else:
                print(f"❌ Failed to load persons: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error loading known faces: {e}")
            return False
    
    def initialize_camera(self, camera_index=0):
        """Initialize webcam"""
        try:
            self.video_capture = cv2.VideoCapture(camera_index)
            
            if not self.video_capture.isOpened():
                print(f"❌ Could not open camera {camera_index}")
                return False
            
            # Set camera properties
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            print(f"✅ Camera {camera_index} initialized")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def send_match_to_api(self, person_id, person_name, similarity, face_location):
        """Send match detection to API"""
        try:
            # Check cooldown
            current_time = time.time()
            if person_id in self.last_match_time:
                if current_time - self.last_match_time[person_id] < self.match_cooldown:
                    return  # Skip if within cooldown period
            
            data = {
                'encoding': [0] * 128,  # Dummy encoding (not needed for report)
                'metadata': {
                    'camera_id': CAMERA_ID,
                    'timestamp': datetime.now().isoformat(),
                    'location': 'Webcam',
                    'bbox': face_location,
                    'detection_confidence': float(similarity),
                    'person_id': person_id,
                    'person_name': person_name
                }
            }
            
            response = requests.post(f'{API_URL}/api/recognize', json=data)
            
            if response.status_code == 200:
                print(f"✅ Match reported: {person_name} (similarity: {similarity:.2f})")
                self.last_match_time[person_id] = current_time
            else:
                print(f"⚠️  Failed to report match: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending match to API: {e}")
    
    def process_frame(self, frame):
        """Process a single frame for face detection and recognition"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        face_similarities = []
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=CONFIDENCE_THRESHOLD
            )
            name = "Unknown"
            similarity = 0.0
            person_id = None
            
            if len(self.known_face_encodings) > 0:
                # Calculate face distances
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        person_id = self.known_face_ids[best_match_index]
                        # Convert distance to similarity (0-1)
                        similarity = 1.0 - face_distances[best_match_index]
                        
                        # Send match to API if similarity is high enough
                        if similarity >= CONFIDENCE_THRESHOLD:
                            face_loc = face_locations[len(face_names)]
                            self.send_match_to_api(person_id, name, similarity, {
                                'top': int(face_loc[0] * 4),
                                'right': int(face_loc[1] * 4),
                                'bottom': int(face_loc[2] * 4),
                                'left': int(face_loc[3] * 4)
                            })
            
            face_names.append(name)
            face_similarities.append(similarity)
        
        return face_locations, face_names, face_similarities
    
    def draw_results(self, frame, face_locations, face_names, face_similarities):
        """Draw bounding boxes and labels on frame"""
        for (top, right, bottom, left), name, similarity in zip(face_locations, face_names, face_similarities):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Choose color based on match
            if name != "Unknown":
                color = (0, 255, 0)  # Green for known faces
                label = f"{name} ({similarity:.2f})"
            else:
                color = (0, 0, 255)  # Red for unknown faces
                label = "Unknown"
            
            # Draw box
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw label text
            cv2.putText(frame, label, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        """Main detection loop"""
        print("=" * 50)
        print("Webcam Face Detection & Recognition")
        print("=" * 50)
        
        # Load known faces
        if not self.load_known_faces():
            print("⚠️  Warning: No known faces loaded. Will only detect faces.")
        
        # Initialize camera
        if not self.initialize_camera():
            print("❌ Failed to initialize camera. Exiting.")
            return
        
        print("\n✅ System ready!")
        print("Press 'q' to quit")
        print("Press 'r' to reload known faces")
        print("=" * 50)
        
        try:
            while True:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    print("❌ Failed to grab frame")
                    break
                
                # Process every Nth frame
                if self.frame_count % PROCESS_EVERY_N_FRAMES == 0:
                    face_locations, face_names, face_similarities = self.process_frame(frame)
                    
                    # Draw results
                    frame = self.draw_results(frame, face_locations, face_names, face_similarities)
                
                self.frame_count += 1
                
                # Display frame
                cv2.imshow('Webcam Face Detection', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n👋 Quitting...")
                    break
                elif key == ord('r'):
                    print("\n🔄 Reloading known faces...")
                    self.load_known_faces()
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
        
        finally:
            # Cleanup
            if self.video_capture:
                self.video_capture.release()
            cv2.destroyAllWindows()
            print("✅ Camera released")


if __name__ == '__main__':
    detector = WebcamDetection()
    detector.run()
