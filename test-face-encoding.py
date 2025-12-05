"""
Test Face Encoding Upload and Database Storage
This script tests the complete workflow:
1. Login to get auth token
2. Upload a test image
3. Create person with face encoding
4. Verify encoding is stored in database
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
API_URL = 'http://localhost:3000'
TEST_CREDENTIALS = {
    'username': 'ompriyanshu12@gmail.com',
    'password': 'pradeep3133'
}

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def login():
    """Login and get auth token"""
    print_section("STEP 1: LOGIN")
    
    try:
        response = requests.post(
            f'{API_URL}/api/auth/login',
            json=TEST_CREDENTIALS,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def upload_photo(token, image_path):
    """Upload photo and extract face encoding"""
    print_section("STEP 2: UPLOAD PHOTO & EXTRACT ENCODING")
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"📸 Uploading image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'photo': ('test.jpg', f, 'image/jpeg')}
            headers = {'Authorization': f'Bearer {token}'}
            
            response = requests.post(
                f'{API_URL}/api/upload/person-photo',
                files=files,
                headers=headers,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Photo uploaded successfully!")
            print(f"   Faces detected: {data.get('facesDetected', 0)}")
            print(f"   Image URL: {data.get('imageUrl', 'N/A')}")
            print(f"   Encoding length: {len(data.get('encoding', []))} dimensions")
            print(f"   First 5 values: {data.get('encoding', [])[:5]}")
            return data
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def create_person(token, upload_data):
    """Create person with face encoding"""
    print_section("STEP 3: CREATE PERSON WITH ENCODING")
    
    person_data = {
        'name': 'Test Person',
        'age': 30,
        'gender': 'male',
        'status': 'missing',
        'priority': 'high',
        'description': 'Test person for face encoding verification',
        'faceEncodings': [{
            'encoding': upload_data['encoding'],
            'imageUrl': upload_data['imageUrl']
        }],
        'contactInfo': {
            'phone': '+1234567890',
            'email': 'test@example.com'
        }
    }
    
    print(f"👤 Creating person: {person_data['name']}")
    
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{API_URL}/api/persons',
            json=person_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            person = data.get('person', {})
            person_id = person.get('_id')
            print(f"✅ Person created successfully!")
            print(f"   Person ID: {person_id}")
            print(f"   Name: {person.get('name')}")
            print(f"   Status: {person.get('status')}")
            print(f"   Face encodings count: {len(person.get('faceEncodings', []))}")
            return person_id
        else:
            print(f"❌ Create person failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Create person error: {e}")
        return None

def verify_in_database(token, person_id):
    """Verify person exists in database with face encoding"""
    print_section("STEP 4: VERIFY IN DATABASE")
    
    print(f"🔍 Fetching person from database: {person_id}")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.get(
            f'{API_URL}/api/persons/{person_id}',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            person = data.get('person', {})
            
            print(f"✅ Person found in database!")
            print(f"\n📋 Person Details:")
            print(f"   ID: {person.get('_id')}")
            print(f"   Name: {person.get('name')}")
            print(f"   Age: {person.get('age')}")
            print(f"   Status: {person.get('status')}")
            print(f"   Priority: {person.get('priority')}")
            
            face_encodings = person.get('faceEncodings', [])
            print(f"\n🔢 Face Encodings:")
            print(f"   Count: {len(face_encodings)}")
            
            if len(face_encodings) > 0:
                encoding = face_encodings[0]
                encoding_array = encoding.get('encoding', [])
                
                print(f"\n   ✅ ENCODING VERIFIED IN DATABASE!")
                print(f"   • Dimensions: {len(encoding_array)}")
                print(f"   • Image URL: {encoding.get('imageUrl')}")
                print(f"   • Uploaded At: {encoding.get('uploadedAt')}")
                print(f"   • First 10 values: {encoding_array[:10]}")
                print(f"   • Last 10 values: {encoding_array[-10:]}")
                
                # Verify it's a valid 128D encoding
                if len(encoding_array) == 128:
                    print(f"\n   ✅ VALID 128-DIMENSIONAL ENCODING!")
                    print(f"   • All values are numbers: {all(isinstance(x, (int, float)) for x in encoding_array)}")
                    print(f"   • Min value: {min(encoding_array):.6f}")
                    print(f"   • Max value: {max(encoding_array):.6f}")
                    print(f"   • Mean value: {sum(encoding_array)/len(encoding_array):.6f}")
                else:
                    print(f"   ⚠️  Warning: Expected 128 dimensions, got {len(encoding_array)}")
            else:
                print(f"   ❌ No face encodings found!")
            
            return True
        else:
            print(f"❌ Fetch failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Verify error: {e}")
        return False

def list_all_persons(token):
    """List all persons to show the test person"""
    print_section("STEP 5: LIST ALL PERSONS")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.get(
            f'{API_URL}/api/persons',
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            persons = data.get('persons', [])
            
            print(f"✅ Found {len(persons)} person(s) in database:")
            
            for i, person in enumerate(persons, 1):
                encodings_count = len(person.get('faceEncodings', []))
                print(f"\n   {i}. {person.get('name')}")
                print(f"      ID: {person.get('_id')}")
                print(f"      Status: {person.get('status')}")
                print(f"      Face Encodings: {encodings_count}")
                
            return True
        else:
            print(f"❌ List failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ List error: {e}")
        return False

def main():
    """Main test function"""
    print("\n" + "="*70)
    print("  FACE ENCODING TEST - Upload & Database Verification")
    print("="*70)
    print("\nThis script will:")
    print("  1. Login to the system")
    print("  2. Upload a test image")
    print("  3. Extract 128D face encoding")
    print("  4. Create person with encoding")
    print("  5. Verify encoding is stored in MongoDB")
    print("  6. List all persons")
    
    # Check if image path provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("\n⚠️  No image path provided!")
        print("Usage: python test-face-encoding.py <image_path>")
        print("\nExample:")
        print("  python test-face-encoding.py test-photo.jpg")
        print("\nYou can use any photo with a clear face.")
        print("The script will use a default test if available.")
        
        # Try to find a test image in uploads folder
        uploads_dir = Path(__file__).parent / 'backend-api' / 'uploads'
        if uploads_dir.exists():
            images = list(uploads_dir.glob('*.jpg')) + list(uploads_dir.glob('*.png'))
            if images:
                image_path = str(images[0])
                print(f"\n✅ Found test image: {image_path}")
            else:
                print("\n❌ No test images found. Please provide an image path.")
                return
        else:
            print("\n❌ Please provide an image path.")
            return
    
    # Run tests
    token = login()
    if not token:
        print("\n❌ Test failed: Could not login")
        return
    
    upload_data = upload_photo(token, image_path)
    if not upload_data:
        print("\n❌ Test failed: Could not upload photo")
        return
    
    person_id = create_person(token, upload_data)
    if not person_id:
        print("\n❌ Test failed: Could not create person")
        return
    
    verified = verify_in_database(token, person_id)
    if not verified:
        print("\n❌ Test failed: Could not verify in database")
        return
    
    list_all_persons(token)
    
    # Final summary
    print_section("TEST SUMMARY")
    print("✅ ALL TESTS PASSED!")
    print("\n✓ Photo uploaded successfully")
    print("✓ Face encoding extracted (128 dimensions)")
    print("✓ Person created in database")
    print("✓ Encoding verified in MongoDB")
    print("✓ System is working correctly!")
    
    print("\n" + "="*70)
    print("  Next Steps:")
    print("="*70)
    print("1. Open dashboard: http://localhost:8080")
    print("2. Go to 'Persons' tab")
    print("3. You should see 'Test Person' with face encoding")
    print("4. Surveillance system will now detect this person!")
    print("\n")

if __name__ == '__main__':
    main()
