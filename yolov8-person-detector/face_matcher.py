"""
Face Recognition and Matching Module
"""
import face_recognition
import cv2
import numpy as np
import os
import requests
from pathlib import Path


class FaceMatcher:
    def __init__(self, database_path='database/persons', tolerance=0.6, api_url='http://localhost:5000'):
        """
        Initialize face matcher with database of known faces
        
        Args:
            database_path: Path to folder containing person images (fallback)
            tolerance: Face matching tolerance (lower is stricter, default 0.6)
            api_url: Base URL for the API server
        """
        self.database_path = Path(database_path)
        self.tolerance = tolerance
        self.api_url = api_url
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []  # Store person IDs for reference
        self.load_database()
    
    def load_database(self):
        """Load face encodings from MongoDB API (only missing persons)"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        
        try:
            # Fetch only persons with status=missing from API
            print("Loading missing persons from MongoDB API...")
            response = requests.get(f"{self.api_url}/api/persons?status=missing&limit=1000")
            
            if response.status_code != 200:
                print(f"⚠️  API request failed with status {response.status_code}")
                print("Falling back to local database...")
                self._load_local_database()
                return
            
            data = response.json()
            persons = data.get('persons', [])
            
            if not persons:
                print("⚠️  No missing persons found in database")
                return
            
            print(f"Loading {len(persons)} missing persons from API...")
            
            loaded_count = 0
            for person in persons:
                try:
                    person_name = person.get('name', 'Unknown')
                    person_id = person.get('_id', '')
                    face_encodings = person.get('faceEncodings', [])
                    
                    # Load all face encodings for this person
                    for face_data in face_encodings:
                        encoding = face_data.get('encoding')
                        if encoding and isinstance(encoding, list) and len(encoding) == 128:
                            self.known_face_encodings.append(np.array(encoding))
                            self.known_face_names.append(person_name)
                            self.known_face_ids.append(person_id)
                            loaded_count += 1
                            print(f"  ✓ Loaded: {person_name}")
                        else:
                            print(f"  ✗ Invalid encoding for: {person_name}")
                
                except Exception as e:
                    print(f"  ✗ Error loading person data: {e}")
            
            print(f"✅ Database loaded: {loaded_count} face encodings from {len(persons)} missing persons")
            
        except requests.exceptions.ConnectionError:
            print("⚠️  Could not connect to API server")
            print("Falling back to local database...")
            self._load_local_database()
        except Exception as e:
            print(f"⚠️  Error loading from API: {e}")
            print("Falling back to local database...")
            self._load_local_database()
    
    def _load_local_database(self):
        """Fallback: Load face encodings from local image files"""
        if not self.database_path.exists():
            print(f"Warning: Database path {self.database_path} does not exist")
            return
        
        # Supported image formats
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        # Load all images from database
        image_files = []
        for ext in image_extensions:
            image_files.extend(self.database_path.glob(f'*{ext}'))
            image_files.extend(self.database_path.glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"Warning: No images found in {self.database_path}")
            return
        
        print(f"Loading {len(image_files)} person images from local database...")
        
        for image_path in image_files:
            try:
                # Load image
                image = face_recognition.load_image_file(str(image_path))
                
                # Get face encodings
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Use first face found in image
                    self.known_face_encodings.append(encodings[0])
                    # Use filename (without extension) as person name
                    person_name = image_path.stem.replace('_', ' ').title()
                    self.known_face_names.append(person_name)
                    self.known_face_ids.append('')  # No ID for local files
                    print(f"  ✓ Loaded: {person_name}")
                else:
                    print(f"  ✗ No face found in: {image_path.name}")
            except Exception as e:
                print(f"  ✗ Error loading {image_path.name}: {e}")
        
        print(f"Local database loaded: {len(self.known_face_encodings)} persons")
    
    def match_face(self, person_image):
        """
        Match a person image against the database
        
        Args:
            person_image: Cropped person image (numpy array)
            
        Returns:
            Tuple of (matched_name, confidence) or (None, 0) if no match
        """
        if not self.known_face_encodings:
            return None, 0
        
        # Convert BGR to RGB if needed
        if len(person_image.shape) == 3 and person_image.shape[2] == 3:
            rgb_image = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = person_image
        
        # Use HOG model for faster detection (faster on CPU, good accuracy)
        face_locations = face_recognition.face_locations(rgb_image, model='hog', number_of_times_to_upsample=0)
        
        if not face_locations:
            return None, 0
        
        # Get face encodings - only for first face to save time
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations, num_jitters=1)
        
        if not face_encodings:
            return None, 0
        
        # Use the first face found
        face_encoding = face_encodings[0]
        
        # Calculate face distances (vectorized operation - much faster)
        face_distances = face_recognition.face_distance(
            self.known_face_encodings, 
            face_encoding
        )
        
        # Find best match using vectorized comparison
        best_match_index = np.argmin(face_distances)
        best_distance = face_distances[best_match_index]
        
        # Check if distance is within tolerance
        if best_distance <= self.tolerance:
            name = self.known_face_names[best_match_index]
            confidence = 1 - best_distance
            return name, confidence
        
        return None, 0
    
    def reload_database(self):
        """Reload the database (useful for adding new persons without restarting)"""
        print("\nReloading database...")
        self.load_database()
