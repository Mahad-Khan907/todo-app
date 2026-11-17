import requests
import json
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://127.0.0.1:8001"

def get_auth_token():
    """Register a user and get authentication token"""

    # Register user first
    register_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "securepassword123"
    }

    print("Registering user...")
    register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)

    if register_response.status_code in [200, 400]:  # 400 might indicate user already exists
        print("Registration completed (may already exist)")
    else:
        print(f"Registration failed: {register_response.status_code}, {register_response.text}")
        return None

    # Login to get token
    login_data = {
        "username": "testuser@example.com",
        "password": "securepassword123"
    }

    print("Logging in...")
    # Use form-encoded data for login
    login_response = requests.post(
        f"{BASE_URL}/auth/token",
        data=login_data
    )

    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        print("Authentication successful!")
        return access_token
    else:
        print(f"Login failed: {login_response.status_code}, {login_response.text}")
        return None

def test_reminder_and_recurring():
    """Test the reminder and recurring functionality"""

    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to get authentication token")
        return

    # Set headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create a task with reminder for 1 minute from now and recurring enabled
    task_data = {
        "title": "Test Recurring Reminder Task",
        "description": "A test task to verify reminder and recurring functionality",
        "is_recurring": True,
        "recurring_pattern": "daily",
        "reminder_at": (datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S'),  # 1 minute from now
        "priority": "medium",
        "recurrence_id": "test-series-1"  # Link to recurring series
    }

    print("\nCreating task with reminder for 1 minute from now...")
    response = requests.post(f"{BASE_URL}/tasks/", headers=headers, data=json.dumps(task_data))

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        task = response.json()
        print(f"Task created successfully with ID: {task['id']}")
        print(f"Reminder set for: {task['reminder_at']}")
        print(f"Recurring pattern: {task['recurring_pattern']}")
        print(f"Task details: {json.dumps(task, indent=2)}")

        print("\nThe system should now:")
        print("1. Send an email to your account after about 1 minute (if SMTP is configured)")
        print("2. When you complete this task, a new recurring task should be created as incomplete")

        return task, headers
    else:
        print(f"Failed to create task: {response.status_code}, {response.text}")
        return None, None

def complete_task_and_test_recurrence(task, headers):
    """Complete the task to test recurring functionality"""
    if not task:
        return

    print(f"\nCompleting task {task['id']} to test recurring functionality...")

    # Update the task to mark it as completed
    update_data = {
        "completed": True,
        "completed_at": datetime.now().isoformat()
    }

    response = requests.patch(f"{BASE_URL}/tasks/{task['id']}", headers=headers, data=json.dumps(update_data))

    print(f"Completion Status Code: {response.status_code}")
    if response.status_code == 200:
        completed_task = response.json()
        print(f"Task {completed_task['id']} marked as completed")
        print("A new recurring task should be created automatically as incomplete")
    else:
        print(f"Failed to complete task: {response.status_code}, {response.text}")

if __name__ == "__main__":
    task, headers = test_reminder_and_recurring()

    # Uncomment the lines below if you want to test the completion functionality as well
    # Note: This should be done after verifying the reminder functionality
    # complete_task_and_test_recurrence(task, headers)