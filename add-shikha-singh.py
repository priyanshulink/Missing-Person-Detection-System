"""
Add Shikha Singh to the system
Uploads photo and creates person with face encoding
"""

import requests
import json
import base64
from pathlib import Path

API_URL = 'http://localhost:3000'
CREDENTIALS = {
    'username': 'ompriyanshu12@gmail.com',
    'password': 'pradeep3133'
}

def login():
    """Login and get token"""
    print("=" * 70)
    print("STEP 1: LOGIN")
    print("=" * 70)
    
    response = requests.post(f'{API_URL}/api/auth/login', json=CREDENTIALS, timeout=5)
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        return None

def upload_photo(token, image_path):
    """Upload photo and extract face encoding"""
    print("\n" + "=" * 70)
    print("STEP 2: UPLOAD PHOTO & EXTRACT FACE ENCODING")
    print("=" * 70)
    
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return None
    
    print(f"📸 Uploading image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'photo': ('shikha_singh.jpg', f, 'image/jpeg')}
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
            print(f"   Encoding dimensions: {len(data.get('encoding', []))}")
            print(f"   Image URL: {data.get('imageUrl')}")
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
    print("\n" + "=" * 70)
    print("STEP 3: CREATE PERSON - SHIKHA SINGH")
    print("=" * 70)
    
    person_data = {
        'name': 'shikha singh',
        'age': 20,
        'gender': 'male',
        'status': 'missing',
        'priority': 'high',
        'description': 'Person with glasses and beard, wearing red and white shirt',
        'faceEncodings': [{
            'encoding': upload_data['encoding'],
            'imageUrl': upload_data['imageUrl']
        }],
        'contactInfo': {
            'phone': '+91-XXXXXXXXXX',
            'email': 'contact@example.com'
        },
        'lastSeenLocation': 'Unknown'
    }
    
    print(f"👤 Creating person:")
    print(f"   Name: {person_data['name']}")
    print(f"   Age: {person_data['age']}")
    print(f"   Gender: {person_data['gender']}")
    print(f"   Status: {person_data['status']}")
    
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
            
            print(f"\n✅ Person created successfully!")
            print(f"   Person ID: {person_id}")
            print(f"   Name: {person.get('name')}")
            print(f"   Status: {person.get('status')}")
            print(f"   Face encodings: {len(person.get('faceEncodings', []))}")
            
            return person_id
        else:
            print(f"❌ Create person failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Create person error: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("ADD PERSON: SHIKHA SINGH")
    print("=" * 70)
    print("\nThis will:")
    print("1. Login to the system")
    print("2. Upload the photo")
    print("3. Extract 128D face encoding")
    print("4. Create person in database")
    print("5. Surveillance will detect this person automatically")
    print()
    
    # Image path (assuming image is saved in project root)
    image_path = Path(__file__).parent / 'shikha_singh.jpg'
    
    if not image_path.exists():
        print(f"❌ Image not found at: {image_path}")
        print("\nPlease save the image as 'shikha_singh.jpg' in the project folder")
        return
    
    # Login
    token = login()
    if not token:
        print("\n❌ FAILED: Cannot login")
        return
    
    # Upload photo
    upload_data = upload_photo(token, str(image_path))
    if not upload_data:
        print("\n❌ FAILED: Cannot upload photo")
        return
    
    # Create person
    person_id = create_person(token, upload_data)
    if not person_id:
        print("\n❌ FAILED: Cannot create person")
        return
    
    # Success
    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print("\n✅ Shikha Singh added to the system!")
    print("\n📋 What happens now:")
    print("   1. Face encoding is stored in database (128 dimensions)")
    print("   2. Surveillance system will reload persons automatically")
    print("   3. When Shikha Singh appears on webcam:")
    print("      → System will detect the face")
    print("      → Compare with stored encoding")
    print("      → If match ≥45%, alert will be triggered")
    print("      → Dashboard will show: '🚨 shikha singh detected!'")
    print("      → Report will be created")
    print("\n🎥 Surveillance is continuously monitoring!")
    print("   Just show this person to the webcam and watch for alerts.")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
