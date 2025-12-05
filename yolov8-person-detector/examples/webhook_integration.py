"""
Example: Webhook Integration
Send alerts to external systems via HTTP webhooks
"""
import requests
import json
from datetime import datetime


class WebhookAlert:
    def __init__(self, webhook_url):
        """
        Initialize webhook alert system
        
        Args:
            webhook_url: URL to send POST requests to
        """
        self.webhook_url = webhook_url
    
    def send_alert(self, person_name, confidence, image_path=None):
        """
        Send alert to webhook
        
        Args:
            person_name: Name of detected person
            confidence: Confidence score
            image_path: Optional path to captured image
        """
        payload = {
            "event": "person_detected",
            "person_name": person_name,
            "confidence": float(confidence),
            "timestamp": datetime.now().isoformat(),
            "location": "Camera 1"  # Customize as needed
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✓ Webhook sent successfully for {person_name}")
            else:
                print(f"✗ Webhook failed: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Webhook error: {e}")


# Example usage in main.py:
"""
# Add to main.py imports:
from examples.webhook_integration import WebhookAlert

# Initialize in main():
webhook = WebhookAlert("https://your-server.com/api/alerts")

# In detection loop, after match found:
if matched_name:
    webhook.send_alert(matched_name, confidence)
"""


# Example webhook server (Flask):
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/alerts', methods=['POST'])
def receive_alert():
    data = request.json
    print(f"Alert received: {data}")
    
    # Process alert (send email, SMS, log to database, etc.)
    
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(port=5000)
"""
