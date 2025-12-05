"""
Simple script to test if camera is working
"""
import cv2


def test_camera(camera_index=0):
    """Test camera functionality"""
    
    print(f"Testing camera {camera_index}...")
    print("Press 'q' to quit\n")
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        print("\nTroubleshooting:")
        print("  - Make sure no other application is using the camera")
        print("  - Try different camera index (0, 1, 2, etc.)")
        print("  - Check if camera is properly connected")
        return
    
    print("✓ Camera opened successfully")
    print(f"  Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    print(f"  FPS: {int(cap.get(cv2.CAP_PROP_FPS))}")
    print()
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Add text overlay
        cv2.putText(frame, "Camera Test - Press 'q' to quit", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Camera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("\n✓ Camera test complete")


if __name__ == "__main__":
    import sys
    
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_camera.py [camera_index]")
            sys.exit(1)
    
    test_camera(camera_index)
