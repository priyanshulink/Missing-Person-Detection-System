"""
Camera Control Script
Start/Stop individual cameras in the multi-camera system
"""

import requests
import sys

BACKEND_URL = 'http://localhost:3000'

def get_camera_status(camera_id):
    """Get current camera status"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/cameras/{camera_id}')
        if response.status_code == 200:
            camera = response.json()['camera']
            return camera
        else:
            print(f"❌ Camera not found: {camera_id}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def activate_camera(camera_id):
    """Activate (start) a camera"""
    try:
        response = requests.patch(
            f'{BACKEND_URL}/api/cameras/{camera_id}/status',
            json={'status': 'active'}
        )
        if response.status_code == 200:
            print(f"✅ Camera '{camera_id}' activated successfully")
            return True
        else:
            print(f"❌ Failed to activate camera: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def deactivate_camera(camera_id):
    """Deactivate (stop) a camera"""
    try:
        response = requests.patch(
            f'{BACKEND_URL}/api/cameras/{camera_id}/status',
            json={'status': 'inactive'}
        )
        if response.status_code == 200:
            print(f"✅ Camera '{camera_id}' deactivated successfully")
            return True
        else:
            print(f"❌ Failed to deactivate camera: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_cameras():
    """List all cameras"""
    try:
        response = requests.get(f'{BACKEND_URL}/api/cameras')
        if response.status_code == 200:
            cameras = response.json()['cameras']
            print("\n📹 Available Cameras:")
            print("-" * 70)
            for cam in cameras:
                status_icon = "🟢" if cam['status'] == 'active' else "🔴"
                print(f"{status_icon} {cam['cameraId']:15} | {cam['name']:25} | {cam['status']}")
            print("-" * 70)
            return cameras
        else:
            print(f"❌ Failed to fetch cameras: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("="*70)
    print("Camera Control System")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python control_camera.py list")
        print("  python control_camera.py start <camera_id>")
        print("  python control_camera.py stop <camera_id>")
        print("  python control_camera.py status <camera_id>")
        print("\nExamples:")
        print("  python control_camera.py list")
        print("  python control_camera.py start cam02")
        print("  python control_camera.py stop cam02")
        print("  python control_camera.py status cam02")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_cameras()
    
    elif command == 'start':
        if len(sys.argv) < 3:
            print("❌ Please specify camera ID")
            print("Example: python control_camera.py start cam02")
            sys.exit(1)
        
        camera_id = sys.argv[2]
        print(f"\n🔄 Starting camera: {camera_id}")
        activate_camera(camera_id)
        
        # Show updated status
        camera = get_camera_status(camera_id)
        if camera:
            print(f"\nCamera: {camera['name']}")
            print(f"Location: {camera['location']}")
            print(f"Status: {camera['status']}")
    
    elif command == 'stop':
        if len(sys.argv) < 3:
            print("❌ Please specify camera ID")
            print("Example: python control_camera.py stop cam02")
            sys.exit(1)
        
        camera_id = sys.argv[2]
        print(f"\n🔄 Stopping camera: {camera_id}")
        deactivate_camera(camera_id)
        
        # Show updated status
        camera = get_camera_status(camera_id)
        if camera:
            print(f"\nCamera: {camera['name']}")
            print(f"Location: {camera['location']}")
            print(f"Status: {camera['status']}")
    
    elif command == 'status':
        if len(sys.argv) < 3:
            print("❌ Please specify camera ID")
            print("Example: python control_camera.py status cam02")
            sys.exit(1)
        
        camera_id = sys.argv[2]
        camera = get_camera_status(camera_id)
        
        if camera:
            print(f"\n📹 Camera Details:")
            print(f"   ID: {camera['cameraId']}")
            print(f"   Name: {camera['name']}")
            print(f"   Location: {camera['location']}")
            print(f"   Status: {camera['status']}")
            print(f"   Stream URL: {camera['streamUrl']}")
            print(f"   Active: {'Yes' if camera.get('isActive', True) else 'No'}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Valid commands: list, start, stop, status")

if __name__ == "__main__":
    main()
