"""
YOLOv8 Person Detection Module
"""
from ultralytics import YOLO
import cv2
import numpy as np


class PersonDetector:
    def __init__(self, model_name='yolov8n.pt', confidence_threshold=0.5):
        """
        Initialize YOLOv8 person detector
        
        Args:
            model_name: YOLOv8 model variant (yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
            confidence_threshold: Minimum confidence for detection
        """
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold
        self.person_class_id = 0  # COCO dataset class ID for 'person'
        
    def detect_persons(self, frame):
        """
        Detect persons in a frame
        
        Args:
            frame: Input image/frame (numpy array)
            
        Returns:
            List of dictionaries containing detection info:
            [{'bbox': (x1, y1, x2, y2), 'confidence': float, 'cropped_image': np.array}]
        """
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class ID and confidence
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                # Check if it's a person and meets confidence threshold
                if class_id == self.person_class_id and confidence >= self.confidence_threshold:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Ensure coordinates are within frame bounds
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
                    
                    # Crop person from frame
                    cropped_person = frame[y1:y2, x1:x2]
                    
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence,
                        'cropped_image': cropped_person
                    })
        
        return detections
    
    def draw_detections(self, frame, detections, labels=None):
        """
        Draw bounding boxes on frame
        
        Args:
            frame: Input frame
            detections: List of detection dictionaries
            labels: Optional list of labels for each detection
            
        Returns:
            Frame with drawn bounding boxes
        """
        annotated_frame = frame.copy()
        
        for idx, detection in enumerate(detections):
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Determine color and label
            if labels and idx < len(labels):
                color = (0, 255, 0) if labels[idx] else (0, 165, 255)  # Green if matched, Orange if not
                label_text = labels[idx] if labels[idx] else f"Person {confidence:.2f}"
            else:
                color = (0, 165, 255)
                label_text = f"Person {confidence:.2f}"
            
            # Draw bounding box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label background
            label_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), color, -1)
            
            # Draw label text
            cv2.putText(annotated_frame, label_text, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame
