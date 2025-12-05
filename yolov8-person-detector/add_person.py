"""
Utility script to add a person to the database using webcam
"""
import cv2
import os
import face_recognition
from pathlib import Path
from datetime import datetime


def capture_person_image():
    """Capture a person's image from webcam and save to database"""
    
    print("="*60)
    print("Add Person to Database")
    print("="*60)
    
    # Get person name
    person_name = input("\nEnter person's name: ").strip()
    if not person_name:
        print("Error: Name cannot be empty")
        return
    
    # Create database directory if it doesn't exist
    database_path = Path('database/persons')
    database_path.mkdir(parents=True, exist_ok=True)
    
    # Create filename
    filename = person_name.lower().replace(' ', '_') + '.jpg'
    filepath = database_path / filename
    
    # Check if person already exists
    if filepath.exists():
        overwrite = input(f"Person '{person_name}' already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Cancelled")
            return
    
    # Open camera
    print("\nOpening camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("\nInstructions:")
    print("  - Position your face in the center of the frame")
    print("  - Make sure your face is well-lit and clearly visible")
    print("  - Press SPACE to capture")
    print("  - Press ESC to cancel")
    print()
    
    captured = False
    face_detected = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Draw guide rectangle
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        box_size = 300
        
        # Detect face in real-time for instant feedback
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')  # Use HOG for speed
        
        # Update face detection status
        face_detected = len(face_locations) > 0
        
        # Draw guide rectangle (green if face detected, red if not)
        box_color = (0, 255, 0) if face_detected else (0, 0, 255)
        cv2.rectangle(frame, 
                     (center_x - box_size//2, center_y - box_size//2),
                     (center_x + box_size//2, center_y + box_size//2),
                     box_color, 2)
        
        # Draw face rectangles
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Add instructions with face detection status
        status_text = "Face Detected - Ready!" if face_detected else "No Face Detected"
        status_color = (0, 255, 0) if face_detected else (0, 0, 255)
        cv2.putText(frame, status_text, (20, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (20, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Capture Person Image', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            if not face_detected:
                print("\n⚠ Warning: No face detected! Please position your face properly.")
                continue
            
            # Save image
            cv2.imwrite(str(filepath), frame)
            print(f"\n✓ Image saved: {filepath}")
            print("✓ Face encoding will be generated automatically")
            captured = True
            break
        elif key == 27:  # ESC
            print("\nCancelled")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if captured:
        print(f"\n✓ Successfully added '{person_name}' to database")
        print(f"  File: {filepath}")
        print("\nYou can now run main.py to detect this person")


if __name__ == "__main__":
    capture_person_image()
