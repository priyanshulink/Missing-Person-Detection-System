"""
Integrated System - Camera + AI Module
Combines camera capture and AI processing in a single script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'camera-module'))

import cv2
import logging
from main import PersonDetectionAI
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'camera-module'))
from camera_service import CameraService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegratedSystem:
    """Integrated camera and AI processing system"""
    
    def __init__(self):
        self.camera_service = CameraService()
        self.ai_module = PersonDetectionAI()
        self.running = False
    
    def start(self):
        """Start the integrated system"""
        logger.info("Starting Integrated System...")
        
        # Initialize and start camera service
        if not self.camera_service.initialize_cameras():
            logger.error("Failed to initialize cameras")
            return False
        
        self.camera_service.start()
        self.running = True
        
        logger.info("Integrated system started successfully")
        return True
    
    def stop(self):
        """Stop the integrated system"""
        logger.info("Stopping Integrated System...")
        self.running = False
        self.camera_service.stop()
        logger.info("Integrated system stopped")
    
    def run(self):
        """Main processing loop"""
        if not self.start():
            return
        
        try:
            logger.info("Processing started. Press 'q' to quit.")
            
            while self.running:
                # Get frames from all cameras
                frames = self.camera_service.get_all_frames()
                
                if not frames:
                    continue
                
                # Process each camera frame
                for camera_id, frame_data in frames.items():
                    frame = frame_data['frame']
                    timestamp = frame_data['timestamp']
                    
                    # Process frame with AI module
                    results = self.ai_module.process_frame(frame, camera_id)
                    
                    # Draw results on frame
                    annotated_frame = self.ai_module.draw_results(frame, results)
                    
                    # Display frame
                    cv2.imshow(f'Detection - {camera_id}', annotated_frame)
                    
                    # Log matches
                    if results['matches']:
                        for match in results['matches']:
                            logger.info(
                                f"Match found on {camera_id}: {match['name']} "
                                f"(similarity: {match['similarity']:.2f})"
                            )
                
                # Check for quit key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        
        finally:
            self.stop()
            cv2.destroyAllWindows()


def main():
    """Main entry point"""
    system = IntegratedSystem()
    system.run()


if __name__ == "__main__":
    main()
