"""
Simple Face Detection Test
Tests if face_recognition can detect your face
"""

import cv2
import face_recognition
import numpy as np

print("=" * 70)
print("SIMPLE FACE DETECTION TEST")
print("=" * 70)
print("\nOpening webcam...")
print("Press SPACE to test face detection")
print("Press Q to quit")
print("=" * 70)

# Open webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Could not open webcam!")
    exit(1)

print("✅ Webcam opened successfully\n")

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("❌ Failed to grab frame")
        break
    
    # Show frame
    cv2.putText(frame, "Press SPACE to test, Q to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Face Detection Test', frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord(' '):  # Space bar
        print("\n" + "=" * 70)
        print("TESTING FACE DETECTION...")
        print("=" * 70)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        print("\n1. Detecting faces with HOG model...")
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        
        if len(face_locations) == 0:
            print("   ❌ NO FACE DETECTED!")
            print("\n   Troubleshooting:")
            print("   - Move closer to camera")
            print("   - Ensure good lighting")
            print("   - Face the camera directly")
            print("   - Remove obstructions (hands, hair)")
            
            # Try CNN model (more accurate but slower)
            print("\n2. Trying CNN model (more accurate)...")
            face_locations = face_recognition.face_locations(rgb_frame, model='cnn')
            
            if len(face_locations) == 0:
                print("   ❌ Still no face detected with CNN model")
                print("\n   Your face might be:")
                print("   - Too far from camera")
                print("   - At a bad angle")
                print("   - In poor lighting")
                print("   - Partially obscured")
            else:
                print(f"   ✅ CNN model detected {len(face_locations)} face(s)!")
                for i, (top, right, bottom, left) in enumerate(face_locations, 1):
                    print(f"   Face {i}: top={top}, right={right}, bottom={bottom}, left={left}")
                    # Draw box
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        else:
            print(f"   ✅ FACE DETECTED! Found {len(face_locations)} face(s)")
            
            for i, (top, right, bottom, left) in enumerate(face_locations, 1):
                print(f"\n   Face {i}:")
                print(f"     Location: top={top}, right={right}, bottom={bottom}, left={left}")
                print(f"     Size: {right-left}x{bottom-top} pixels")
                
                # Draw box
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
                cv2.putText(frame, f"Face {i}", (left, top-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Generate encodings
            print("\n3. Generating face encodings...")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if len(face_encodings) == 0:
                print("   ❌ Could not generate face encodings!")
            else:
                print(f"   ✅ Generated {len(face_encodings)} encoding(s)")
                for i, encoding in enumerate(face_encodings, 1):
                    print(f"   Encoding {i}: {len(encoding)} dimensions")
                    print(f"   First 5 values: {encoding[:5]}")
                
                print("\n   ✅ SUCCESS! Your face can be detected and encoded!")
                print("   This means the system should work.")
        
        # Show result
        cv2.imshow('Face Detection Test', frame)
        cv2.waitKey(2000)  # Show for 2 seconds
        
        print("\n" + "=" * 70)
        print("Press SPACE to test again, Q to quit")
        print("=" * 70)
    
    elif key == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
print("\n✅ Test complete")
