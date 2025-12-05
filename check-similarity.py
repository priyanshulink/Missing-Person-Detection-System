"""
Check Face Similarity Against Database
Shows exact match percentages
"""

import cv2
import face_recognition
import numpy as np
import requests
import sys

API_URL = 'http://localhost:3000'
CREDENTIALS = {'username': 'ompriyanshu12@gmail.com', 'password': 'pradeep3133'}

print("=" * 80)
print("FACE SIMILARITY CHECKER")
print("=" * 80)

# Login
print("\n1. Logging in...")
try:
    response = requests.post(f'{API_URL}/api/auth/login', json=CREDENTIALS, timeout=5)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        sys.exit(1)
    token = response.json().get('token')
    print("✅ Logged in successfully")
except Exception as e:
    print(f"❌ Login error: {e}")
    sys.exit(1)

# Load persons
print("\n2. Loading persons from database...")
try:
    response = requests.get(f'{API_URL}/api/persons', timeout=5)
    if response.status_code != 200:
        print(f"❌ Failed to load persons: {response.status_code}")
        sys.exit(1)
    
    persons = response.json().get('persons', [])
    
    known_encodings = []
    known_names = []
    known_ids = []
    
    for person in persons:
        for enc_data in person.get('faceEncodings', []):
            encoding = enc_data.get('encoding')
            if encoding and len(encoding) == 128:
                known_encodings.append(np.array(encoding))
                known_names.append(person['name'])
                known_ids.append(person['_id'])
    
    print(f"✅ Loaded {len(known_encodings)} face encodings from {len(persons)} persons")
    
    if len(known_encodings) == 0:
        print("❌ No persons with face encodings in database!")
        sys.exit(1)
    
    print("\nPersons in database:")
    for i, name in enumerate(set(known_names), 1):
        count = known_names.count(name)
        print(f"   {i}. {name} ({count} encoding(s))")

except Exception as e:
    print(f"❌ Error loading persons: {e}")
    sys.exit(1)

# Open webcam
print("\n3. Opening webcam...")
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ Could not open webcam!")
    sys.exit(1)

print("✅ Webcam opened")
print("\n" + "=" * 80)
print("INSTRUCTIONS:")
print("- Position your face clearly in front of camera")
print("- Press SPACE to check similarity")
print("- Press Q to quit")
print("=" * 80)

test_count = 0

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("❌ Failed to grab frame")
        break
    
    # Add instructions on frame
    cv2.putText(frame, "Press SPACE to check similarity, Q to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow('Similarity Checker', frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord(' '):  # Space bar
        test_count += 1
        print("\n" + "=" * 80)
        print(f"TEST #{test_count}")
        print("=" * 80)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        print("\nStep 1: Detecting faces...")
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        
        if len(face_locations) == 0:
            print("❌ NO FACE DETECTED!")
            print("   Try: Move closer, better lighting, face camera directly")
            continue
        
        print(f"✅ Detected {len(face_locations)} face(s)")
        
        # Generate encodings
        print("\nStep 2: Generating face encodings...")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        if len(face_encodings) == 0:
            print("❌ Could not generate encodings!")
            continue
        
        print(f"✅ Generated {len(face_encodings)} encoding(s)")
        
        # Compare each detected face
        for face_idx, face_encoding in enumerate(face_encodings, 1):
            print(f"\n{'='*80}")
            print(f"FACE #{face_idx} - SIMILARITY RESULTS:")
            print(f"{'='*80}")
            
            # Compare with all known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.40)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            # Show results for each person
            print("\nComparison with each person:")
            print("-" * 80)
            
            results = []
            for i, (name, distance, match) in enumerate(zip(known_names, face_distances, matches)):
                similarity = (1.0 - distance) * 100
                match_status = "✅ MATCH!" if match else "❌ No match"
                results.append((name, similarity, match, distance))
                print(f"{i+1}. {name:20s} | Similarity: {similarity:5.1f}% | {match_status}")
            
            # Find best match
            if len(face_distances) > 0:
                best_idx = np.argmin(face_distances)
                best_name = known_names[best_idx]
                best_similarity = (1.0 - face_distances[best_idx]) * 100
                best_match = matches[best_idx]
                
                print("\n" + "=" * 80)
                print("BEST MATCH:")
                print("=" * 80)
                print(f"Name:       {best_name}")
                print(f"Similarity: {best_similarity:.1f}%")
                print(f"Threshold:  40.0% (need ≥40% to trigger alert)")
                print(f"Status:     {'✅ WOULD TRIGGER ALERT!' if best_match else '❌ Below threshold - No alert'}")
                
                if not best_match:
                    print(f"\nTo trigger alert, need: ≥40.0%")
                    print(f"You got:                {best_similarity:.1f}%")
                    print(f"Difference:             {40.0 - best_similarity:.1f}% short")
                    print("\nSuggestions:")
                    print("- Add more photos of this person from different angles")
                    print("- Lower threshold to 35% or 30%")
                    print("- Improve lighting conditions")
                    print("- Try different facial expression")
                
                # Draw box on frame
                top, right, bottom, left = face_locations[face_idx-1]
                color = (0, 255, 0) if best_match else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                label = f"{best_name} {best_similarity:.0f}%"
                cv2.putText(frame, label, (left, top-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Show result frame
        cv2.imshow('Similarity Checker', frame)
        cv2.waitKey(3000)  # Show for 3 seconds
        
        print("\n" + "=" * 80)
        print("Press SPACE to test again, Q to quit")
        print("=" * 80)
    
    elif key == ord('q'):
        print("\n👋 Exiting...")
        break

video_capture.release()
cv2.destroyAllWindows()
print("\n✅ Test complete")
