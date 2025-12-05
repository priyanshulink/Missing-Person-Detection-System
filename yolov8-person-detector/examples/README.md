# Integration Examples

This folder contains example code for integrating the person detection system with external services.

## Available Examples

### 1. Webhook Integration (`webhook_integration.py`)

Send HTTP POST requests to external services when a person is detected.

**Use cases:**
- Integrate with home automation systems
- Trigger IoT devices
- Log to external databases
- Connect to monitoring dashboards

**Setup:**
```python
from examples.webhook_integration import WebhookAlert

webhook = WebhookAlert("https://your-server.com/api/alerts")
webhook.send_alert(person_name, confidence)
```

### 2. Email Notifications (`email_notification.py`)

Send email alerts with optional image attachments.

**Use cases:**
- Security notifications
- Remote monitoring
- Alert multiple recipients
- Keep email logs

**Setup:**
```python
from examples.email_notification import EmailAlert

email_alert = EmailAlert(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    sender_email='your-email@gmail.com',
    sender_password='your-app-password'
)

email_alert.send_alert(person_name, confidence, 'recipient@example.com', frame)
```

## How to Use

### Step 1: Install Additional Dependencies

```bash
pip install requests  # For webhook integration
```

### Step 2: Import in main.py

Add to the top of `main.py`:
```python
from examples.webhook_integration import WebhookAlert
# or
from examples.email_notification import EmailAlert
```

### Step 3: Initialize in main()

```python
# After initializing alert_system
webhook = WebhookAlert("https://your-webhook-url.com/alerts")
# or
email_alert = EmailAlert(smtp_server, smtp_port, email, password)
```

### Step 4: Trigger in Detection Loop

In the detection loop where alerts are triggered:
```python
if matched_name:
    # Existing alert
    if alert_system.trigger_alert(matched_name, confidence):
        # Add webhook
        webhook.send_alert(matched_name, confidence)
        # or email
        email_alert.send_alert(matched_name, confidence, 'you@example.com', frame)
```

## Security Best Practices

### For Webhooks:
- Use HTTPS endpoints
- Implement authentication tokens
- Validate SSL certificates
- Rate limit requests

### For Email:
- Use app passwords, not account passwords
- Store credentials in environment variables
- Use encrypted connections (TLS)
- Don't commit credentials to git

### Example with Environment Variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

email_alert = EmailAlert(
    smtp_server=os.getenv('SMTP_SERVER'),
    smtp_port=int(os.getenv('SMTP_PORT')),
    sender_email=os.getenv('SENDER_EMAIL'),
    sender_password=os.getenv('SENDER_PASSWORD')
)
```

Create `.env` file:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

## Creating Your Own Integration

Template for custom integrations:

```python
class CustomAlert:
    def __init__(self, config):
        self.config = config
    
    def send_alert(self, person_name, confidence, **kwargs):
        try:
            # Your custom logic here
            print(f"Custom alert for {person_name}")
        except Exception as e:
            print(f"Error: {e}")
```

## Popular Integration Ideas

1. **Telegram Bot** - Send messages to Telegram
2. **Discord Webhook** - Post to Discord channel
3. **Slack Notification** - Alert Slack workspace
4. **SMS via Twilio** - Send text messages
5. **Push Notifications** - Mobile app alerts
6. **Database Logging** - Store in PostgreSQL/MongoDB
7. **Home Assistant** - Smart home integration
8. **MQTT Broker** - IoT device communication

## Need Help?

Check the main README.md or create an issue on the project repository.
