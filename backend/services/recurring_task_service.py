"""
Recurring Task Service for processing task events and creating new instances with Dapr pub/sub support
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import text
from fastapi import FastAPI, Request
import uvicorn
import os
from dapr.ext.fastapi import DaprApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
dapr_app = DaprApp(app)

# Global service instance
recurring_service = None

class RecurringTaskService:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

    def calculate_next_occurrence(self, task: Dict[str, Any]) -> datetime:
        """
        Calculate the next occurrence date based on the recurring pattern
        """
        current_date = datetime.now()
        pattern = task.get('recurring_pattern', 'daily')

        if pattern == "daily":
            return current_date + timedelta(days=1)
        elif pattern == "weekly":
            return current_date + timedelta(weeks=1)
        elif pattern == "monthly":
            # For monthly, we'll add roughly a month (30 days)
            return current_date + timedelta(days=30)
        elif pattern == "custom":
            # For custom patterns, we could implement more complex logic
            # For now, default to daily
            return current_date + timedelta(days=1)
        else:
            # Default to next day if pattern is invalid
            return current_date + timedelta(days=1)

    async def create_next_task_instance(self, original_task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create the next instance of a recurring task
        """
        try:
            next_due_date = self.calculate_next_occurrence(original_task)

            # Create new task with same properties but updated dates
            new_task = {
                "title": original_task.get("title"),
                "description": original_task.get("description"),
                "completed": False,
                "priority": original_task.get("priority", "medium"),
                "due_date": next_due_date.isoformat() if next_due_date else None,
                "completed_at": None,
                "is_recurring": original_task.get("is_recurring", False),
                "recurring_pattern": original_task.get("recurring_pattern"),
                "recurrence_id": original_task.get("recurrence_id") or original_task.get("id"),
                "reminder_at": original_task.get("reminder_at"),  # Carry over reminder settings if any
                "last_notified": None,
                "reminder_sent": False,  # New task hasn't had its reminder sent yet
                "user_id": original_task.get("user_id"),
                "tags": original_task.get("tags", [])
            }

            # In a real implementation, we would save this to the database
            logger.info(f"Created next instance for recurring task: {new_task['title']}")

            return new_task
        except Exception as e:
            logger.error(f"Error creating next task instance: {e}")
            return None

    async def handle_task_event(self, task_event: Dict[str, Any]):
        """
        Handle incoming task events from the pub/sub system
        """
        try:
            event_type = task_event.get("event_type")
            task_data = task_event.get("task_data")

            logger.info(f"Processing task event: {event_type} for task {task_data.get('id')}")

            if event_type == "task_completed" and task_data.get("is_recurring"):
                # Create the next instance of the recurring task
                new_task = await self.create_next_task_instance(task_data)

                if new_task:
                    # In a real implementation, we would save this to the database
                    # and potentially publish an event about the new task creation
                    logger.info(f"Created new task instance: {new_task['title']}")

                    # Publish event about new task creation
                    # await self.publish_new_task_event(new_task)

                    return {
                        "status": "success",
                        "action": "created_next_instance",
                        "new_task_id": new_task.get("id")
                    }

            return {"status": "processed", "event_type": event_type}

        except Exception as e:
            logger.error(f"Error handling task event: {e}")
            return {"status": "error", "error": str(e)}

    async def publish_new_task_event(self, new_task: Dict[str, Any]):
        """
        Publish an event about the creation of a new task instance
        """
        try:
            # In a real implementation, this would publish to Dapr pub/sub
            event_data = {
                "event_type": "new_task_created",
                "task_data": new_task,
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Published new task event: {new_task.get('title')}")
            return True
        except Exception as e:
            logger.error(f"Error publishing new task event: {e}")
            return False

@app.on_event("startup")
async def startup_event():
    """
    Initialize the recurring task service on app startup
    """
    global recurring_service
    database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    recurring_service = RecurringTaskService(database_url)
    logger.info("Recurring task service initialized")

@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr pub/sub subscription endpoint
    """
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "tasks",
            "route": "/task"
        }
    ]

@app.post("/task")
async def handle_task(request: Request):
    """
    Handle task events from Dapr pub/sub
    """
    try:
        task_event = await request.json()
        logger.info(f"Received task event: {task_event}")

        if recurring_service is None:
            logger.error("Recurring service not initialized")
            return {"status": "error", "error": "Service not initialized"}

        result = await recurring_service.handle_task_event(task_event)
        logger.info(f"Processed task event result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing task event: {e}")
        return {"status": "error", "error": str(e)}

# Keep the old function for backward compatibility if needed
async def listen_for_task_events():
    """
    Listen for task events from Dapr pub/sub
    """
    database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    recurring_service = RecurringTaskService(database_url)

    logger.info("Recurring task service started, listening for task events...")

    # This function is no longer needed since we use FastAPI
    # but keeping for potential backward compatibility
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)