"""
Test All Camera Streams
Tests connectivity to all configured cameras
"""

import cv2
import time

# Camera configurations from seed-cameras.js
cameras = [
    {
        'id': 'cam02',
        'name': 'Library Hall Camera',
        'url': 'http://10.28.71.10:8080/video'
    },
    {
        'id': 'cam_local',
        'name': 'Local Webcam',
        'url': '0'  # Default webcam
    }
]

print("="*60)
print("Multi-Camera Stream Test")
print("="*60)

results = []

for camera in cameras:
    print(f"\n📹 Testing: {camera['name']} ({camera['id']})")
    print(f"   URL: {camera['url']}")
    
    # Convert '0' to integer for local webcam
    stream_url = int(camera['url']) if camera['url'].isdigit() else camera['url']
    
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print(f"   ❌ FAILED: Could not connect")
        results.append({
            'camera': camera['name'],
            'status': 'FAILED',
            'error': 'Connection failed'
        })
        continue
    
    # Try to read a frame
    ret, frame = cap.read()
    
    if not ret:
        print(f"   ❌ FAILED: Could not read frame")
        results.append({
            'camera': camera['name'],
            'status': 'FAILED',
            'error': 'Cannot read frames'
        })
        cap.release()
        continue
    
    # Get frame info
    height, width = frame.shape[:2]
    
    print(f"   ✅ SUCCESS")
    print(f"   Resolution: {width}x{height}")
    
    results.append({
        'camera': camera['name'],
        'status': 'SUCCESS',
        'resolution': f"{width}x{height}"
    })
    
    cap.release()
    time.sleep(0.5)

# Print summary
print("\n" + "="*60)
print("Test Summary")
print("="*60)

for result in results:
    status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
    print(f"{status_icon} {result['camera']}: {result['status']}")
    if result['status'] == 'SUCCESS':
        print(f"   Resolution: {result['resolution']}")
    else:
        print(f"   Error: {result['error']}")

# Count successes
success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
total_count = len(results)

print(f"\n📊 Results: {success_count}/{total_count} cameras working")

if success_count == total_count:
    print("\n✅ All cameras are working correctly!")
    print("You can now proceed with the multi-camera surveillance system.")
elif success_count > 0:
    print("\n⚠️  Some cameras are working, but not all.")
    print("Check the failed cameras and try again.")
else:
    print("\n❌ No cameras are working.")
    print("Please check your camera configurations and network connectivity.")
