"""
Test Live Face Detection
Capture a frame from webcam and test against database
"""

import cv2
import face_recognition
import numpy as np
import requests

API_URL = 'http://localhost:3000'
CREDENTIALS = {'username': 'ompriyanshu12@gmail.com', 'password': 'pradeep3133'}

def login():
    response = requests.post(f'{API_URL}/api/auth/login', json=CREDENTIALS)
    return response.json().get('token')

def load_persons(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_URL}/api/persons', headers=headers)
    persons = response.json().get('persons', [])
    
    encodings = []
    names = []
    
    for person in persons:
        for enc_data in person.get('faceEncodings', []):
            encoding = enc_data.get('encoding')
            if encoding and len(encoding) == 128:
                encodings.append(np.array(encoding))
                names.append(person['name'])
    
    return encodings, names

def test_detection():
    print("=" * 70)
    print("LIVE FACE DETECTION TEST")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    token = login()
    print("   ✅ Logged in")
    
    # Load persons
    print("\n2. Loading persons from database...")
    known_encodings, known_names = load_persons(token)
    print(f"   ✅ Loaded {len(known_encodings)} face encodings")
    
    if len(known_encodings) == 0:
        print("\n❌ No persons with face encodings in database!")
        return
    
    # Open webcam
    print("\n3. Opening webcam...")
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("   ❌ Could not open webcam")
        return
    
    print("   ✅ Webcam opened")
    print("\n" + "=" * 70)
    print("INSTRUCTIONS:")
    print("- Position your face in front of camera")
    print("- Press SPACE to test detection")
    print("- Press Q to quit")
    print("=" * 70)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Show frame
        cv2.imshow('Test Detection - Press SPACE to test, Q to quit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space bar
            print("\n" + "=" * 70)
            print("TESTING CURRENT FRAME...")
            print("=" * 70)
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            print("1. Detecting faces...")
            face_locations = face_recognition.face_locations(rgb_frame)
            print(f"   Found {len(face_locations)} face(s)")
            
            if len(face_locations) == 0:
                print("   ❌ No face detected! Try:")
                print("      - Move closer to camera")
                print("      - Ensure good lighting")
                print("      - Face the camera directly")
                continue
            
            # Generate encodings
            print("\n2. Generating face encodings...")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            print(f"   Generated {len(face_encodings)} encoding(s)")
            
            # Test each face
            for i, face_encoding in enumerate(face_encodings, 1):
                print(f"\n3. Testing face #{i}...")
                
                # Compare
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                print(f"   Distances to known faces:")
                for j, (name, distance) in enumerate(zip(known_names, face_distances)):
                    similarity = (1.0 - distance) * 100
                    match_status = "✅ MATCH!" if matches[j] else "❌ No match"
                    print(f"     {name}: {similarity:.1f}% similarity - {match_status}")
                
                # Best match
                if len(face_distances) > 0:
                    best_match_idx = np.argmin(face_distances)
                    best_distance = face_distances[best_match_idx]
                    best_similarity = (1.0 - best_distance) * 100
                    best_name = known_names[best_match_idx]
                    
                    print(f"\n   BEST MATCH:")
                    print(f"     Name: {best_name}")
                    print(f"     Similarity: {best_similarity:.1f}%")
                    print(f"     Threshold: 45%")
                    
                    if matches[best_match_idx]:
                        print(f"     ✅ WOULD TRIGGER ALERT!")
                    else:
                        print(f"     ❌ Below threshold - No alert")
                        print(f"     Need: ≥45% similarity")
                        print(f"     Got: {best_similarity:.1f}%")
            
            print("\n" + "=" * 70)
            print("Press SPACE to test again, Q to quit")
            print("=" * 70)
        
        elif key == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    print("\n✅ Test complete")

if __name__ == '__main__':
    test_detection()
