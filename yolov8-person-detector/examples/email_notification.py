"""
Example: Email Notification
Send email alerts when person is detected
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import cv2


class EmailAlert:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        """
        Initialize email alert system
        
        Args:
            smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
            smtp_port: SMTP port (e.g., 587 for TLS)
            sender_email: Your email address
            sender_password: Your email password or app password
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_alert(self, person_name, confidence, recipient_email, image=None):
        """
        Send email alert
        
        Args:
            person_name: Name of detected person
            confidence: Confidence score
            recipient_email: Email to send alert to
            image: Optional numpy array of captured frame
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"🚨 Alert: {person_name} Detected"
            
            # Email body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = f"""
            <html>
            <body>
                <h2>Person Detection Alert</h2>
                <p><strong>Person:</strong> {person_name}</p>
                <p><strong>Confidence:</strong> {confidence:.1%}</p>
                <p><strong>Time:</strong> {timestamp}</p>
                <p><strong>Location:</strong> Main Camera</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach image if provided
            if image is not None:
                _, img_encoded = cv2.imencode('.jpg', image)
                img_bytes = img_encoded.tobytes()
                
                image_part = MIMEImage(img_bytes, name='detection.jpg')
                msg.attach(image_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✓ Email sent to {recipient_email}")
            
        except Exception as e:
            print(f"✗ Email error: {e}")


# Example usage:
"""
# Configuration (use environment variables in production!)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'  # Use app password for Gmail
RECIPIENT_EMAIL = 'recipient@example.com'

# Initialize
email_alert = EmailAlert(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD)

# In detection loop:
if matched_name:
    email_alert.send_alert(matched_name, confidence, RECIPIENT_EMAIL, frame)
"""

# Gmail setup instructions:
"""
For Gmail:
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Use app password instead of regular password
"""
