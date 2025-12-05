"""
Disable local webcam camera
Run this to prevent webcam from auto-starting
"""

import requests

BACKEND_URL = 'http://localhost:3000'

def disable_webcam():
    """Disable the local webcam camera"""
    try:
        # Get all cameras
        response = requests.get(f'{BACKEND_URL}/api/cameras')
        if response.status_code == 200:
            data = response.json()
            cameras = data.get('cameras', [])
            
            # Find webcam camera
            for camera in cameras:
                if 'cam_local' in camera.get('cameraId', '') or 'webcam' in camera.get('name', '').lower():
                    camera_id = camera['_id']
                    print(f"Found webcam: {camera['name']} ({camera_id})")
                    
                    # Update to inactive
                    update_response = requests.put(
                        f'{BACKEND_URL}/api/cameras/{camera_id}',
                        json={'isActive': False, 'status': 'inactive'}
                    )
                    
                    if update_response.status_code == 200:
                        print(f"✅ Disabled webcam: {camera['name']}")
                    else:
                        print(f"❌ Failed to disable: {update_response.status_code}")
            
            print("\n✅ Done! Restart your app to apply changes.")
        else:
            print(f"❌ Failed to get cameras: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("="*50)
    print("  Disable Local Webcam Camera")
    print("="*50)
    print()
    disable_webcam()
