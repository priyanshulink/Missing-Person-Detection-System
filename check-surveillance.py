"""
Check Surveillance System Status
Diagnose why face detection is not working
"""

import requests
import json

API_URL = 'http://localhost:3000'

# Login credentials
CREDENTIALS = {
    'username': 'ompriyanshu12@gmail.com',
    'password': 'pradeep3133'
}

def login():
    """Login and get token"""
    print("=" * 70)
    print("STEP 1: LOGIN")
    print("=" * 70)
    
    try:
        response = requests.post(f'{API_URL}/api/auth/login', json=CREDENTIALS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Login successful")
            return token
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_persons(token):
    """Check persons in database"""
    print("\n" + "=" * 70)
    print("STEP 2: CHECK PERSONS IN DATABASE")
    print("=" * 70)
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_URL}/api/persons', headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            persons = data.get('persons', [])
            
            print(f"\n✅ Found {len(persons)} person(s) in database\n")
            
            if len(persons) == 0:
                print("❌ NO PERSONS FOUND!")
                print("   You need to add a person with photo first.")
                return False
            
            for i, person in enumerate(persons, 1):
                encodings = person.get('faceEncodings', [])
                print(f"{i}. Name: {person.get('name')}")
                print(f"   ID: {person.get('_id')}")
                print(f"   Status: {person.get('status')}")
                print(f"   Face Encodings: {len(encodings)}")
                
                if len(encodings) == 0:
                    print(f"   ❌ WARNING: No face encodings! Person won't be detected.")
                else:
                    for j, enc in enumerate(encodings, 1):
                        encoding_array = enc.get('encoding', [])
                        print(f"   Encoding {j}:")
                        print(f"     - Dimensions: {len(encoding_array)}")
                        print(f"     - Image: {enc.get('imageUrl')}")
                        
                        if len(encoding_array) != 128:
                            print(f"     ❌ INVALID: Expected 128 dimensions, got {len(encoding_array)}")
                        else:
                            print(f"     ✅ Valid 128D encoding")
                print()
            
            return len(persons) > 0 and any(len(p.get('faceEncodings', [])) > 0 for p in persons)
        else:
            print(f"❌ Failed to fetch persons: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_surveillance_status(token):
    """Check if surveillance is running"""
    print("=" * 70)
    print("STEP 3: CHECK SURVEILLANCE STATUS")
    print("=" * 70)
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{API_URL}/api/surveillance/status', headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            pid = data.get('pid')
            
            if status == 'running':
                print(f"✅ Surveillance is RUNNING (PID: {pid})")
                return True
            else:
                print(f"❌ Surveillance is NOT running")
                print(f"   Status: {status}")
                return False
        else:
            print(f"⚠️  Could not check status: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Error checking status: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("SURVEILLANCE SYSTEM DIAGNOSTIC")
    print("=" * 70)
    print("\nChecking why face detection is not working...\n")
    
    # Step 1: Login
    token = login()
    if not token:
        print("\n❌ FAILED: Cannot login")
        return
    
    # Step 2: Check persons
    has_persons = check_persons(token)
    if not has_persons:
        print("\n" + "=" * 70)
        print("DIAGNOSIS")
        print("=" * 70)
        print("❌ PROBLEM: No persons with face encodings in database")
        print("\nSOLUTION:")
        print("1. Go to dashboard: http://localhost:8080")
        print("2. Click 'Persons' → 'Add Person'")
        print("3. Capture/upload your photo")
        print("4. Fill form and save")
        print("5. Make sure you see 'Face encoding extracted successfully'")
        return
    
    # Step 3: Check surveillance
    is_running = check_surveillance_status(token)
    
    # Final diagnosis
    print("\n" + "=" * 70)
    print("DIAGNOSIS")
    print("=" * 70)
    
    if has_persons and is_running:
        print("✅ System looks good!")
        print("\nPossible reasons for no detection:")
        print("1. Face not clearly visible to camera")
        print("2. Different lighting conditions")
        print("3. Different angle than uploaded photo")
        print("4. Confidence threshold too high")
        print("\nTROUBLESHOOTING:")
        print("- Make sure your face is well-lit")
        print("- Face the camera directly")
        print("- Try uploading multiple photos from different angles")
        print("- Check surveillance window for detection boxes")
    elif has_persons and not is_running:
        print("❌ PROBLEM: Surveillance is not running")
        print("\nSOLUTION:")
        print("1. Check if Python surveillance script is running")
        print("2. Look for 'YOLO Surveillance' window")
        print("3. Check backend terminal for errors")
        print("4. Try restarting: Logout and login again")
    else:
        print("❌ PROBLEM: System not properly configured")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Check the surveillance window (should show video)")
    print("2. Look for green/red boxes around faces")
    print("3. Check backend terminal for detection messages")
    print("4. If still not working, check logs above for specific issues")
    print()

if __name__ == '__main__':
    main()
