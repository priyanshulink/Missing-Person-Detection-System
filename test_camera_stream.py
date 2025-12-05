"""
Camera Stream Test Script
Tests camera connection before YOLO integration
"""

import cv2
import sys

# Camera stream URL from your configuration
CAMERA_URL = "http://10.28.71.10:8080/video"

print("="*60)
print("Camera Stream Test")
print("="*60)
print(f"\nTesting connection to: {CAMERA_URL}")
print("\nPress 'q' to quit\n")

# Try to open the camera stream
cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("❌ ERROR: Could not open camera stream")
    print("\nTroubleshooting:")
    print("1. Check if the camera IP is correct: 10.28.71.10")
    print("2. Verify the camera is on the same network")
    print("3. Test the URL in a web browser: http://10.28.71.10:8080/video")
    print("4. Check if IP Webcam app is running on the phone")
    print("5. Ensure firewall is not blocking the connection")
    sys.exit(1)

print("✅ Camera stream opened successfully!")
print("Displaying live video... (Press 'q' to quit)\n")

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("⚠️  Warning: Failed to read frame")
        continue
    
    frame_count += 1
    
    # Add frame counter to display
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Add camera info
    cv2.putText(frame, "Library Hall Camera", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Display the frame
    cv2.imshow("Live Stream - Library Hall Camera", frame)
    
    # Print status every 100 frames
    if frame_count % 100 == 0:
        print(f"✅ Streaming... Frame {frame_count}")
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n🛑 Stopping stream...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

print(f"\n✅ Test completed successfully!")
print(f"Total frames received: {frame_count}")
print("\nCamera stream is working correctly! ✓")
