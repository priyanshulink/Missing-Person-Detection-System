"""
Camera Module - CCTV Video Capture Service
Captures live video feed from CCTV cameras and provides frames for AI processing
"""

import cv2
import json
import time
import logging
from typing import List, Dict, Optional
import threading
from queue import Queue
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CameraService:
    """Service to capture video from multiple CCTV cameras"""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize camera service
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.cameras: Dict[str, cv2.VideoCapture] = {}
        self.frame_queues: Dict[str, Queue] = {}
        self.running = False
        self.threads: List[threading.Thread] = []
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found, using defaults")
            return {
                "camera_sources": [0],  # Default to webcam
                "frame_width": 640,
                "frame_height": 480,
                "fps": 30,
                "buffer_size": 10
            }
    
    def initialize_cameras(self) -> bool:
        """
        Initialize all camera sources
        
        Returns:
            bool: True if at least one camera initialized successfully
        """
        camera_sources = self.config.get('camera_sources', [0])
        success_count = 0
        
        for idx, source in enumerate(camera_sources):
            camera_id = f"camera_{idx}"
            try:
                cap = cv2.VideoCapture(source)
                
                if not cap.isOpened():
                    logger.error(f"Failed to open camera source: {source}")
                    continue
                
                # Set camera properties
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get('frame_width', 640))
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get('frame_height', 480))
                cap.set(cv2.CAP_PROP_FPS, self.config.get('fps', 30))
                
                self.cameras[camera_id] = cap
                self.frame_queues[camera_id] = Queue(maxsize=self.config.get('buffer_size', 10))
                
                logger.info(f"Camera {camera_id} initialized: {source}")
                success_count += 1
                
            except Exception as e:
                logger.error(f"Error initializing camera {source}: {str(e)}")
        
        return success_count > 0
    
    def _capture_frames(self, camera_id: str):
        """
        Capture frames from a specific camera
        
        Args:
            camera_id: Identifier for the camera
        """
        cap = self.cameras[camera_id]
        frame_queue = self.frame_queues[camera_id]
        
        logger.info(f"Started capture thread for {camera_id}")
        
        while self.running:
            try:
                ret, frame = cap.read()
                
                if not ret:
                    logger.warning(f"Failed to read frame from {camera_id}")
                    time.sleep(0.1)
                    continue
                
                # Add timestamp to frame metadata
                frame_data = {
                    'frame': frame,
                    'timestamp': datetime.now().isoformat(),
                    'camera_id': camera_id
                }
                
                # Add to queue (non-blocking)
                if frame_queue.full():
                    try:
                        frame_queue.get_nowait()  # Remove oldest frame
                    except:
                        pass
                
                frame_queue.put(frame_data)
                
            except Exception as e:
                logger.error(f"Error capturing frame from {camera_id}: {str(e)}")
                time.sleep(0.1)
        
        logger.info(f"Stopped capture thread for {camera_id}")
    
    def start(self):
        """Start capturing from all cameras"""
        if self.running:
            logger.warning("Camera service already running")
            return
        
        if not self.cameras:
            if not self.initialize_cameras():
                logger.error("No cameras available to start")
                return
        
        self.running = True
        
        # Start capture thread for each camera
        for camera_id in self.cameras.keys():
            thread = threading.Thread(
                target=self._capture_frames,
                args=(camera_id,),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
        
        logger.info(f"Camera service started with {len(self.cameras)} cameras")
    
    def stop(self):
        """Stop capturing from all cameras"""
        logger.info("Stopping camera service...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=2.0)
        
        # Release all cameras
        for camera_id, cap in self.cameras.items():
            cap.release()
            logger.info(f"Released {camera_id}")
        
        self.cameras.clear()
        self.frame_queues.clear()
        self.threads.clear()
        
        logger.info("Camera service stopped")
    
    def get_frame(self, camera_id: str, timeout: float = 1.0) -> Optional[Dict]:
        """
        Get the latest frame from a specific camera
        
        Args:
            camera_id: Identifier for the camera
            timeout: Maximum time to wait for a frame
            
        Returns:
            Dictionary containing frame and metadata, or None
        """
        if camera_id not in self.frame_queues:
            logger.error(f"Camera {camera_id} not found")
            return None
        
        try:
            frame_data = self.frame_queues[camera_id].get(timeout=timeout)
            return frame_data
        except:
            return None
    
    def get_all_frames(self) -> Dict[str, Dict]:
        """
        Get latest frames from all cameras
        
        Returns:
            Dictionary mapping camera_id to frame data
        """
        frames = {}
        for camera_id in self.cameras.keys():
            frame_data = self.get_frame(camera_id, timeout=0.1)
            if frame_data:
                frames[camera_id] = frame_data
        return frames
    
    def get_camera_info(self) -> List[Dict]:
        """
        Get information about all active cameras
        
        Returns:
            List of dictionaries containing camera information
        """
        info = []
        for camera_id, cap in self.cameras.items():
            info.append({
                'camera_id': camera_id,
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': int(cap.get(cv2.CAP_PROP_FPS)),
                'is_opened': cap.isOpened()
            })
        return info


def main():
    """Main function to run camera service"""
    logger.info("Starting Camera Service...")
    
    # Create camera service
    camera_service = CameraService()
    
    # Initialize and start
    if not camera_service.initialize_cameras():
        logger.error("Failed to initialize cameras")
        return
    
    camera_service.start()
    
    # Display camera info
    camera_info = camera_service.get_camera_info()
    logger.info(f"Active cameras: {camera_info}")
    
    try:
        # Keep service running and display frames
        logger.info("Camera service running. Press Ctrl+C to stop.")
        
        while True:
            frames = camera_service.get_all_frames()
            
            for camera_id, frame_data in frames.items():
                frame = frame_data['frame']
                timestamp = frame_data['timestamp']
                
                # Display frame with info
                cv2.putText(
                    frame,
                    f"{camera_id} - {timestamp}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
                
                cv2.imshow(camera_id, frame)
            
            # Break on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(0.03)  # ~30 FPS display
    
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    
    finally:
        # Cleanup
        camera_service.stop()
        cv2.destroyAllWindows()
        logger.info("Camera service terminated")


if __name__ == "__main__":
    main()
