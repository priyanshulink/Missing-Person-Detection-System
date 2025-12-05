"""
AI/ML Module - Person Detection and Face Recognition
Uses YOLOv8 for person detection and face_recognition for face encoding
"""

import cv2
import json
import logging
import requests
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import time
import face_recognition
from ultralytics import YOLO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PersonDetectionAI:
    """AI module for person detection and face recognition"""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize AI module
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.yolo_model = None
        self.backend_api_url = self.config.get('backend_api_url', 'http://localhost:3000')
        self.confidence_threshold = self.config.get('confidence_threshold', 0.6)
        self.face_detection_model = self.config.get('face_detection_model', 'hog')
        
        self._initialize_models()
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found, using defaults")
            return {
                "backend_api_url": "http://localhost:3000",
                "confidence_threshold": 0.6,
                "yolo_model": "yolov8n.pt",
                "face_detection_model": "hog",
                "min_face_size": 50
            }
    
    def _initialize_models(self):
        """Initialize YOLO and face recognition models"""
        try:
            # Load YOLOv8 model
            model_path = self.config.get('yolo_model', 'yolov8n.pt')
            logger.info(f"Loading YOLOv8 model: {model_path}")
            self.yolo_model = YOLO(model_path)
            logger.info("YOLOv8 model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise
    
    def detect_persons(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect persons in a frame using YOLOv8
        
        Args:
            frame: Input image frame
            
        Returns:
            List of detected person bounding boxes with confidence scores
        """
        if self.yolo_model is None:
            logger.error("YOLO model not initialized")
            return []
        
        try:
            # Run inference
            results = self.yolo_model(frame, verbose=False)
            
            persons = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Class 0 is 'person' in COCO dataset
                    if int(box.cls[0]) == 0:
                        confidence = float(box.conf[0])
                        
                        if confidence >= self.confidence_threshold:
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            
                            persons.append({
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'confidence': confidence
                            })
            
            return persons
            
        except Exception as e:
            logger.error(f"Error detecting persons: {str(e)}")
            return []
    
    def extract_face_encodings(self, frame: np.ndarray, person_bbox: List[int]) -> Optional[List[float]]:
        """
        Extract face encoding from a person's bounding box
        
        Args:
            frame: Input image frame
            person_bbox: Bounding box [x1, y1, x2, y2] of detected person
            
        Returns:
            Face encoding as list of floats, or None if no face detected
        """
        try:
            x1, y1, x2, y2 = person_bbox
            
            # Crop person region
            person_img = frame[y1:y2, x1:x2]
            
            # Check if crop is valid
            if person_img.size == 0:
                return None
            
            # Convert BGR to RGB (face_recognition uses RGB)
            rgb_img = cv2.cvtColor(person_img, cv2.COLOR_BGR2RGB)
            
            # Detect face locations
            face_locations = face_recognition.face_locations(
                rgb_img,
                model=self.face_detection_model
            )
            
            if not face_locations:
                logger.debug("No face detected in person bounding box")
                return None
            
            # Get face encoding for the first detected face
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
            
            if face_encodings:
                # Convert to list for JSON serialization
                encoding = face_encodings[0].tolist()
                return encoding
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting face encoding: {str(e)}")
            return None
    
    def send_to_backend(self, encoding: List[float], metadata: Dict) -> Optional[Dict]:
        """
        Send face encoding to backend API for identification
        
        Args:
            encoding: Face encoding vector
            metadata: Additional metadata (camera_id, timestamp, etc.)
            
        Returns:
            Response from backend API or None on error
        """
        try:
            url = f"{self.backend_api_url}/api/recognize"
            
            payload = {
                'encoding': encoding,
                'metadata': metadata
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Backend returned status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to backend: {str(e)}")
            return None
    
    def process_frame(self, frame: np.ndarray, camera_id: str = "camera_0") -> Dict:
        """
        Process a single frame: detect persons, extract faces, send to backend
        
        Args:
            frame: Input video frame
            camera_id: Identifier for the camera source
            
        Returns:
            Processing results including detections and matches
        """
        timestamp = datetime.now().isoformat()
        
        results = {
            'camera_id': camera_id,
            'timestamp': timestamp,
            'persons_detected': 0,
            'faces_extracted': 0,
            'matches': []
        }
        
        # Detect persons
        persons = self.detect_persons(frame)
        results['persons_detected'] = len(persons)
        
        if not persons:
            return results
        
        # Process each detected person
        for idx, person in enumerate(persons):
            bbox = person['bbox']
            confidence = person['confidence']
            
            # Extract face encoding
            encoding = self.extract_face_encodings(frame, bbox)
            
            if encoding is not None:
                results['faces_extracted'] += 1
                
                # Send to backend for identification
                metadata = {
                    'camera_id': camera_id,
                    'timestamp': timestamp,
                    'bbox': bbox,
                    'detection_confidence': confidence
                }
                
                response = self.send_to_backend(encoding, metadata)
                
                if response and response.get('match_found'):
                    results['matches'].append({
                        'person_id': response.get('person_id'),
                        'name': response.get('name'),
                        'similarity': response.get('similarity'),
                        'bbox': bbox
                    })
                    
                    logger.info(f"Match found: {response.get('name')} (similarity: {response.get('similarity'):.2f})")
        
        return results
    
    def draw_results(self, frame: np.ndarray, results: Dict) -> np.ndarray:
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            results: Processing results from process_frame
            
        Returns:
            Frame with drawn annotations
        """
        annotated_frame = frame.copy()
        
        # Draw matches
        for match in results.get('matches', []):
            bbox = match['bbox']
            name = match['name']
            similarity = match['similarity']
            
            x1, y1, x2, y2 = bbox
            
            # Draw bounding box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label = f"{name} ({similarity:.2f})"
            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        # Draw info
        info_text = f"Persons: {results['persons_detected']} | Faces: {results['faces_extracted']} | Matches: {len(results['matches'])}"
        cv2.putText(
            annotated_frame,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        return annotated_frame


def main():
    """Main function to run AI module with camera feed"""
    logger.info("Starting AI/ML Module...")
    
    # Initialize AI module
    ai_module = PersonDetectionAI()
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Failed to open camera")
        return
    
    logger.info("AI module running. Press 'q' to quit.")
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                logger.warning("Failed to read frame")
                break
            
            # Process frame
            results = ai_module.process_frame(frame, camera_id="camera_0")
            
            # Draw results
            annotated_frame = ai_module.draw_results(frame, results)
            
            # Display
            cv2.imshow('AI Module - Person Detection', annotated_frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("AI module terminated")


if __name__ == "__main__":
    main()
