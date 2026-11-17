"""
Notification Service for handling reminder events with Dapr pub/sub support
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, Request
import uvicorn
from dapr.ext.fastapi import DaprApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
dapr_app = DaprApp(app)

class NotificationService:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        # In a real implementation, these would come from environment/secrets
        self.username = None
        self.password = None

    async def send_reminder_email(self, user_email: str, task_title: str, task_description: str = ""):
        """
        Send reminder email to the user
        """
        try:
            # In a real implementation, we would use a proper email library
            # For now, we'll just log the action
            logger.info(f"Sending reminder email to {user_email} for task '{task_title}'")

            # Here would be the actual email sending logic
            # import smtplib
            # from email.mime.text import MIMEText
            # from email.mime.multipart import MIMEMultipart

            return True
        except Exception as e:
            logger.error(f"Error sending reminder email: {e}")
            return False

    async def handle_reminder_event(self, reminder_data: Dict[str, Any]):
        """
        Handle incoming reminder events from the pub/sub system
        """
        try:
            user_email = reminder_data.get("user_email")
            task_title = reminder_data.get("task_title")
            task_description = reminder_data.get("task_description", "")
            task_id = reminder_data.get("task_id")

            logger.info(f"Processing reminder event for task {task_id}: {task_title}")

            # Send the reminder notification
            success = await self.send_reminder_email(user_email, task_title, task_description)

            if success:
                logger.info(f"Reminder successfully sent for task {task_id}")
                return {"status": "sent", "task_id": task_id}
            else:
                logger.error(f"Failed to send reminder for task {task_id}")
                return {"status": "failed", "task_id": task_id}

        except Exception as e:
            logger.error(f"Error handling reminder event: {e}")
            return {"status": "error", "error": str(e)}

@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr pub/sub subscription endpoint
    """
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "reminders",
            "route": "/reminder"
        }
    ]

@app.post("/reminder")
async def handle_reminder(request: Request):
    """
    Handle reminder events from Dapr pub/sub
    """
    try:
        reminder_data = await request.json()
        logger.info(f"Received reminder event: {reminder_data}")

        notification_service = NotificationService()
        result = await notification_service.handle_reminder_event(reminder_data)

        logger.info(f"Processed reminder event result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing reminder event: {e}")
        return {"status": "error", "error": str(e)}

# Keep the old function for backward compatibility if needed
async def listen_for_reminder_events():
    """
    Listen for reminder events from Dapr pub/sub
    """
    logger.info("Notification service started, listening for reminder events...")

    # This function is no longer needed since we use FastAPI
    # but keeping for potential backward compatibility
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)