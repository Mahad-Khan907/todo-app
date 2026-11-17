import requests
import json
from datetime import datetime, timedelta

# Test the reminder and recurring task functionality
url = "http://127.0.0.1:8001/tasks/"

# Sample task data with reminder set to 1 minute from now and recurring enabled
task_data = {
    "title": "Test Recurring Reminder Task",
    "description": "A test task to verify reminder and recurring functionality",
    "is_recurring": True,
    "recurring_pattern": "daily",
    "reminder_at": (datetime.utcnow() + timedelta(minutes=1)).isoformat(),  # 1 minute from now
    "priority": "medium",
    "recurrence_id": "test-series-1"  # Link to recurring series
}

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYjgxNzQwYS00MjhiLTRlOTctODQ0Ni03MDM2NjM1NjE2OTQiLCJleHAiOjE3Njk5MzYwNzN9._6Ue9cJg5vPgNYg3CePs9cCFZSjBmDrXPXAq3tAVAM8",
    "Content-Type": "application/json"
}

print("Creating task with reminder for 1 minute from now...")
try:
    response = requests.post(url, headers=headers, data=json.dumps(task_data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        task = response.json()
        print(f"Task created successfully with ID: {task['id']}")
        print(f"Reminder set for: {task['reminder_at']}")
        print(f"Recurring pattern: {task['recurring_pattern']}")

        # Wait for 1-2 minutes and then check if email was sent and new task was created
        print("\nThe system should now:")
        print("1. Send an email to your account after about 1 minute")
        print("2. When you complete this task, a new recurring task should be created as incomplete")

    else:
        print("Failed to create task")

except Exception as e:
    print(f"Error: {e}")