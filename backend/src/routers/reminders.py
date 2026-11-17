"""
API Router for Reminder Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..models import Task, TaskPublic, User
from ..database import get_session
from ..auth import get_current_user
from ..utils.reminders import (
    get_pending_reminders,
    get_overdue_reminders,
    mark_reminder_as_notified,
    schedule_reminder
)

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/schedule")
async def schedule_reminder_endpoint(
    task_id: int,
    reminder_time: str,  # ISO format string
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Schedule a reminder for a specific task.

    Args:
        task_id: ID of the task to schedule a reminder for
        reminder_time: ISO format string for when to remind
        current_user: The authenticated user
        session: Database session dependency

    Returns:
        Success message with reminder details
    """
    # Validate reminder_time format
    try:
        reminder_datetime = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid datetime format. Use ISO format (e.g., 2023-12-01T10:30:00)"
        )

    # Get the task to ensure it exists and belongs to the user
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if str(task.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to schedule reminder for this task"
        )

    # Schedule the reminder
    success = schedule_reminder(task, reminder_datetime, session)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule reminder"
        )

    return {
        "message": "Reminder scheduled successfully",
        "task_id": task_id,
        "reminder_time": reminder_datetime.isoformat()
    }


@router.get("/pending", response_model=List[TaskPublic])
async def get_pending_reminders_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all pending reminders for the current user.

    Args:
        current_user: The authenticated user
        session: Database session dependency

    Returns:
        List of tasks with pending reminders
    """
    pending_reminders = get_pending_reminders(str(current_user.id), session)
    return pending_reminders


@router.get("/overdue", response_model=List[TaskPublic])
async def get_overdue_reminders_endpoint(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all overdue reminders for the current user.

    Args:
        current_user: The authenticated user
        session: Database session dependency

    Returns:
        List of tasks with overdue reminders
    """
    overdue_reminders = get_overdue_reminders(str(current_user.id), session)
    return overdue_reminders


@router.delete("/{reminder_id}")
async def cancel_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Cancel a scheduled reminder by marking the task as notified.

    Args:
        reminder_id: ID of the task with the reminder to cancel
        current_user: The authenticated user
        session: Database session dependency

    Returns:
        Success message
    """
    # Get the task to ensure it exists and belongs to the user
    task = session.get(Task, reminder_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if str(task.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel reminder for this task"
        )

    # Mark reminder as notified (effectively cancelling it)
    success = mark_reminder_as_notified(reminder_id, session)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel reminder"
        )

    return {"message": "Reminder cancelled successfully"}