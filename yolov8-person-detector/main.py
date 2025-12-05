"""
YOLOv8 Person Detection and Recognition System
Main Application
"""
import cv2
import time
from person_detector import PersonDetector
from face_matcher import FaceMatcher
from alert_system import AlertSystem
from datetime import datetime


# Configuration
CAMERA_INDEX = 0
CAMERA_NAME = 'Main Entrance Camera'  # Name of the camera
CAMERA_LOCATION = 'Building A - Main Entrance'  # Physical location of the camera
CONFIDENCE_THRESHOLD = 0.5
FACE_MATCH_TOLERANCE = 0.6
ALERT_COOLDOWN = 5  # seconds
DATABASE_PATH = 'database/persons'
API_URL = 'http://localhost:5000'  # Backend API URL
AUTO_RELOAD_INTERVAL = 30  # seconds - automatically reload database every 30 seconds
YOLO_MODEL = 'yolov8n.pt'  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
FRAME_SKIP = 3  # Process every Nth frame for face matching (increased for better performance)
RESIZE_MAX_WIDTH = 1280  # Maximum frame width for processing


def main():
    """Main application loop"""
    print("="*60)
    print("YOLOv8 Person Detection and Recognition System")
    print("="*60)
    
    # Initialize components
    print("\n[1/4] Initializing YOLOv8 person detector...")
    detector = PersonDetector(
        model_name=YOLO_MODEL,
        confidence_threshold=CONFIDENCE_THRESHOLD
    )
    
    print("[2/4] Loading face recognition database...")
    matcher = FaceMatcher(
        database_path=DATABASE_PATH,
        tolerance=FACE_MATCH_TOLERANCE,
        api_url=API_URL
    )
    
    print("[3/4] Initializing alert system...")
    alert_system = AlertSystem(cooldown_seconds=ALERT_COOLDOWN)
    
    print("[4/4] Opening camera...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {CAMERA_INDEX}")
        return
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for lower latency
    
    print("\n✓ System ready!")
    print("\nControls:")
    print("  - Press 'q' to quit")
    print("  - Press 'r' to reload database (refresh missing persons from API)")
    print("  - Press 's' to save screenshot")
    print("  - Press 'c' to clear alert cooldowns")
    print(f"\n🔄 Auto-reload: Database will refresh every {AUTO_RELOAD_INTERVAL} seconds")
    print("="*60 + "\n")
    
    # Performance tracking
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0
    frame_count = 0
    
    # Active alerts (for banner display)
    active_alerts = {}
    
    # Cache for last detections to reduce processing
    last_labels = []
    
    # Auto-reload tracking
    last_reload_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            frame_count += 1
            current_time = time.time()
            
            # Auto-reload database at specified interval
            if AUTO_RELOAD_INTERVAL > 0 and (current_time - last_reload_time) >= AUTO_RELOAD_INTERVAL:
                print(f"\n🔄 Auto-reloading database... (every {AUTO_RELOAD_INTERVAL}s)")
                matcher.reload_database()
                last_reload_time = current_time
            
            # Detect persons in frame
            detections = detector.detect_persons(frame)
            
            # Only perform face matching every FRAME_SKIP frames to improve performance
            if frame_count % FRAME_SKIP == 0:
                labels = []
                
                for detection in detections:
                    cropped_person = detection['cropped_image']
                    
                    # Skip if cropped image is too small
                    if cropped_person.shape[0] < 60 or cropped_person.shape[1] < 60:
                        labels.append(None)
                        continue
                    
                    # Resize large images for faster face matching
                    if cropped_person.shape[0] > 400 or cropped_person.shape[1] > 400:
                        scale = 400 / max(cropped_person.shape[0], cropped_person.shape[1])
                        new_width = int(cropped_person.shape[1] * scale)
                        new_height = int(cropped_person.shape[0] * scale)
                        cropped_person = cv2.resize(cropped_person, (new_width, new_height))
                    
                    # Match face
                    matched_name, confidence = matcher.match_face(cropped_person)
                    
                    if matched_name:
                        label = f"{matched_name} ({confidence:.1%})"
                        labels.append(label)
                        
                        # Trigger alert with camera info
                        if alert_system.trigger_alert(matched_name, confidence, CAMERA_NAME, CAMERA_LOCATION):
                            active_alerts[matched_name] = {
                                'time': current_time,
                                'confidence': confidence
                            }
                    else:
                        labels.append(None)
                
                # Cache labels for next frames
                last_labels = labels
            else:
                # Use cached labels from previous frame
                labels = last_labels if len(last_labels) == len(detections) else [None] * len(detections)
            
            # Draw detections
            annotated_frame = detector.draw_detections(frame, detections, labels)
            
            # Draw alert banners for recent alerts
            alerts_to_remove = []
            for person_name, alert_info in active_alerts.items():
                if current_time - alert_info['time'] < 3:  # Show banner for 3 seconds
                    annotated_frame = alert_system.draw_alert_banner(
                        annotated_frame, 
                        person_name, 
                        alert_info['confidence'],
                        CAMERA_NAME,
                        CAMERA_LOCATION
                    )
                else:
                    alerts_to_remove.append(person_name)
            
            # Remove expired alert banners
            for person_name in alerts_to_remove:
                del active_alerts[person_name]
            
            # Calculate FPS
            fps_counter += 1
            if fps_counter >= 30:
                fps = fps_counter / (time.time() - fps_start_time)
                fps_start_time = time.time()
                fps_counter = 0
            
            # Draw info panel
            info_text = [
                f"FPS: {fps:.1f}",
                f"Persons detected: {len(detections)}",
                f"Database: {len(matcher.known_face_names)} persons",
                f"Time: {datetime.now().strftime('%H:%M:%S')}"
            ]
            
            y_offset = annotated_frame.shape[0] - 120
            for i, text in enumerate(info_text):
                cv2.putText(annotated_frame, text, (10, y_offset + i*25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('YOLOv8 Person Detection & Recognition', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('r'):
                print("\n🔄 Manual reload - Reloading database...")
                matcher.reload_database()
                last_reload_time = current_time  # Reset auto-reload timer
            elif key == ord('s'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"\n✓ Screenshot saved: {filename}")
            elif key == ord('c'):
                print("\nClearing alert cooldowns...")
                alert_system.clear_cooldowns()
                active_alerts.clear()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        # Cleanup
        print("\nCleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        
        # Print alert log
        alert_log = alert_system.get_alert_log()
        if alert_log:
            print("\n" + "="*60)
            print("Alert Log:")
            print("="*60)
            for alert in alert_log:
                print(alert)
        
        print("\n✓ System shutdown complete")


if __name__ == "__main__":
    main()
