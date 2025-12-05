"""
Alert System for Person Detection
"""
import pygame
import time
from datetime import datetime
import os


class AlertSystem:
    def __init__(self, cooldown_seconds=5):
        """
        Initialize alert system
        
        Args:
            cooldown_seconds: Minimum seconds between alerts for same person
        """
        # Initialize pygame mixer for audio alerts
        pygame.mixer.init()
        
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = {}
        self.alert_log = []
        
        # Create a simple beep sound
        self.create_alert_sound()
    
    def create_alert_sound(self):
        """Create a simple alert beep sound"""
        try:
            # Create a simple beep using pygame
            sample_rate = 22050
            duration = 0.3
            frequency = 800
            
            # Generate beep sound
            n_samples = int(round(duration * sample_rate))
            buf = []
            for i in range(n_samples):
                value = int(32767.0 * 0.3 * 
                           (1.0 if (i // (sample_rate // frequency)) % 2 == 0 else -1.0))
                buf.append([value, value])
            
            sound_array = pygame.sndarray.make_sound(buf)
            self.alert_sound = sound_array
        except Exception as e:
            print(f"Warning: Could not create alert sound: {e}")
            self.alert_sound = None
    
    def trigger_alert(self, person_name, confidence, camera_name=None, camera_location=None):
        """
        Trigger an alert for detected person
        
        Args:
            person_name: Name of detected person
            confidence: Confidence score of match
            camera_name: Name of the camera (optional)
            camera_location: Location of the camera (optional)
            
        Returns:
            True if alert was triggered, False if in cooldown
        """
        current_time = time.time()
        
        # Check cooldown
        if person_name in self.last_alert_time:
            time_since_last = current_time - self.last_alert_time[person_name]
            if time_since_last < self.cooldown_seconds:
                return False
        
        # Update last alert time
        self.last_alert_time[person_name] = current_time
        
        # Log alert
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"[{timestamp}] ALERT: {person_name} detected (confidence: {confidence:.2%})"
        
        # Add camera info if provided
        if camera_name:
            alert_message += f" | Camera: {camera_name}"
        if camera_location:
            alert_message += f" | Location: {camera_location}"
        
        self.alert_log.append(alert_message)
        print(f"\n{'='*60}")
        print(f"🚨 {alert_message}")
        print(f"{'='*60}\n")
        
        # Play sound alert
        self.play_sound_alert()
        
        return True
    
    def play_sound_alert(self):
        """Play audio alert"""
        try:
            if self.alert_sound:
                self.alert_sound.play()
        except Exception as e:
            print(f"Warning: Could not play alert sound: {e}")
    
    def get_alert_log(self):
        """Get all alerts"""
        return self.alert_log
    
    def clear_cooldowns(self):
        """Clear all cooldowns"""
        self.last_alert_time.clear()
    
    def draw_alert_banner(self, frame, person_name, confidence, camera_name=None, camera_location=None):
        """
        Draw alert banner on frame
        
        Args:
            frame: Input frame
            person_name: Name of detected person
            confidence: Confidence score
            camera_name: Name of the camera (optional)
            camera_location: Location of the camera (optional)
            
        Returns:
            Frame with alert banner
        """
        import cv2
        
        height, width = frame.shape[:2]
        
        # Calculate banner height based on content
        banner_height = 110 if (camera_name or camera_location) else 80
        
        # Create semi-transparent red overlay at top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, banner_height), (0, 0, 255), -1)
        frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)
        
        # Alert text
        alert_text = f"ALERT: {person_name} DETECTED!"
        confidence_text = f"Confidence: {confidence:.1%}"
        
        # Draw text
        cv2.putText(frame, alert_text, (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        cv2.putText(frame, confidence_text, (20, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add camera info if provided
        y_offset = 90
        if camera_name:
            camera_text = f"Camera: {camera_name}"
            cv2.putText(frame, camera_text, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if camera_location:
            location_text = f"Location: {camera_location}"
            cv2.putText(frame, location_text, (width - 500, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
