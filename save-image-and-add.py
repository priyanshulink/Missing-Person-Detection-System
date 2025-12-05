"""
Save the uploaded image and add person to system
"""

import requests
import json
from pathlib import Path
import shutil

API_URL = 'http://localhost:3000'
CREDENTIALS = {
    'username': 'ompriyanshu12@gmail.com',
    'password': 'pradeep3133'
}

def login():
    response = requests.post(f'{API_URL}/api/auth/login', json=CREDENTIALS, timeout=5)
    if response.status_code == 200:
        return response.json().get('token')
    return None

def upload_and_create(token, image_path):
    """Upload photo and create person"""
    
    print("=" * 70)
    print("ADDING: SHIKHA SINGH")
    print("=" * 70)
    
    # Upload photo
    print("\n📸 Uploading photo...")
    with open(image_path, 'rb') as f:
        files = {'photo': ('shikha_singh.jpg', f, 'image/jpeg')}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f'{API_URL}/api/upload/person-photo',
            files=files,
            headers=headers,
            timeout=30
        )
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.text}")
        return False
    
    upload_data = response.json()
    print(f"✅ Face encoding extracted!")
    print(f"   Dimensions: {len(upload_data.get('encoding', []))}")
    print(f"   Faces detected: {upload_data.get('facesDetected')}")
    
    # Create person
    print("\n👤 Creating person...")
    person_data = {
        'name': 'shikha singh',
        'age': 20,
        'gender': 'male',
        'status': 'missing',
        'priority': 'high',
        'description': 'Person with glasses and beard',
        'faceEncodings': [{
            'encoding': upload_data['encoding'],
            'imageUrl': upload_data['imageUrl']
        }]
    }
    
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
        person = response.json().get('person', {})
        print(f"✅ Person created!")
        print(f"   ID: {person.get('_id')}")
        print(f"   Name: {person.get('name')}")
        
        print("\n" + "=" * 70)
        print("SUCCESS! 🎉")
        print("=" * 70)
        print("\n✅ Shikha Singh is now in the system")
        print("✅ Surveillance is monitoring continuously")
        print("✅ When this person appears on webcam:")
        print("   → Face will be detected")
        print("   → Compared with stored encoding")
        print("   → Alert triggered if match ≥45%")
        print("\n🎥 Show this person to the webcam to test!")
        return True
    else:
        print(f"❌ Create failed: {response.text}")
        return False

def main():
    # Check if image exists
    image_path = Path(__file__).parent / 'shikha_singh.jpg'
    
    if not image_path.exists():
        print("❌ Image 'shikha_singh.jpg' not found in project folder")
        print("\nPlease:")
        print("1. Save the uploaded image as 'shikha_singh.jpg'")
        print("2. Place it in: c:\\Users\\91900\\Downloads\\project\\")
        print("3. Run this script again")
        return
    
    # Login
    print("🔐 Logging in...")
    token = login()
    if not token:
        print("❌ Login failed")
        return
    print("✅ Logged in\n")
    
    # Upload and create
    upload_and_create(token, str(image_path))

if __name__ == '__main__':
    main()
