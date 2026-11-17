"""
Utility functions for processing reminders
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from ..models import Task
from ..database import engine


def get_pending_reminders(user_id: str, session: Session = None) -> List[Task]:
    """
    Get all pending reminders for a specific user

    Args:
        user_id: The user ID to get reminders for
        session: Database session (will be created if not provided)

    Returns:
        List of tasks that have pending reminders
    """
    own_session = False
    if session is None:
        session = Session(engine)
        own_session = True

    try:
        now = datetime.utcnow()

        # Optimized query to get pending reminders for a user
        pending_reminders = session.exec(
            select(Task).where(
                Task.user_id == user_id,
                Task.reminder_at.is_not(None),
                Task.reminder_at >= now,  # Only get future reminders
                Task.last_notified.is_(None)
            )
        ).all()

        return pending_reminders
    finally:
        if own_session:
            session.close()


def get_overdue_reminders(user_id: str, session: Session = None) -> List[Task]:
    """
    Get all overdue reminders for a specific user

    Args:
        user_id: The user ID to get overdue reminders for
        session: Database session (will be created if not provided)

    Returns:
        List of tasks that have overdue reminders
    """
    own_session = False
    if session is None:
        session = Session(engine)
        own_session = True

    try:
        now = datetime.utcnow()

        # Find tasks with reminder_at that has passed and not yet notified
        overdue_reminders = session.exec(
            select(Task).where(
                Task.user_id == user_id,
                Task.reminder_at.is_not(None),
                Task.reminder_at < now,
                Task.last_notified.is_(None)
            )
        ).all()

        return overdue_reminders
    finally:
        if own_session:
            session.close()


def check_reminder_status(task: Task) -> str:
    """
    Check the status of a task's reminder

    Args:
        task: The task to check

    Returns:
        str: Status of the reminder ('pending', 'overdue', 'notified', 'none')
    """
    if not task.reminder_at:
        return 'none'

    now = datetime.utcnow()

    if task.last_notified:
        return 'notified'
    elif task.reminder_at <= now:
        return 'overdue'
    else:
        return 'pending'


def calculate_time_until_reminder(task: Task) -> Optional[timedelta]:
    """
    Calculate the time remaining until a reminder

    Args:
        task: The task with a reminder

    Returns:
        timedelta: Time until reminder, or None if no reminder or already passed
    """
    if not task.reminder_at:
        return None

    now = datetime.utcnow()
    time_diff = task.reminder_at - now

    # Return None if the reminder time has already passed
    if time_diff.total_seconds() <= 0:
        return None

    return time_diff


def format_time_until_reminder(task: Task) -> str:
    """
    Format the time until a reminder in a human-readable way

    Args:
        task: The task with a reminder

    Returns:
        str: Human-readable time until reminder
    """
    time_diff = calculate_time_until_reminder(task)

    if time_diff is None:
        return "Reminder time has passed"

    seconds = int(time_diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}"
    elif hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        return f"{seconds} second{'s' if seconds != 1 else ''}"


def mark_reminder_as_notified(task_id: int, session: Session = None) -> bool:
    """
    Mark a reminder as notified

    Args:
        task_id: The ID of the task whose reminder should be marked as notified
        session: Database session (will be created if not provided)

    Returns:
        bool: True if successful, False otherwise
    """
    own_session = False
    if session is None:
        session = Session(engine)
        own_session = True

    try:
        task = session.get(Task, task_id)
        if task:
            task.last_notified = datetime.utcnow()
            session.add(task)
            session.commit()
            return True
        return False
    except Exception:
        if own_session:
            session.rollback()
        return False
    finally:
        if own_session:
            session.close()


def schedule_reminder(task: Task, reminder_time: datetime, session: Session = None) -> bool:
    """
    Schedule a reminder for a task

    Args:
        task: The task to schedule a reminder for
        reminder_time: The time to schedule the reminder
        session: Database session (will be created if not provided)

    Returns:
        bool: True if successful, False otherwise
    """
    from datetime import timezone

    own_session = False
    if session is None:
        session = Session(engine)
        own_session = True

    try:
        # Validate reminder time (should not be in the past)
        now = datetime.now(timezone.utc)

        # Ensure reminder_time is timezone-aware for comparison
        if reminder_time.tzinfo is None:
            reminder_time = reminder_time.replace(tzinfo=timezone.utc)

        if reminder_time < now:
            raise ValueError("Reminder time cannot be in the past")

        # Update the task's reminder_at field
        task_from_db = session.get(Task, task.id)
        if task_from_db:
            task_from_db.reminder_at = reminder_time
            # Reset notification flags when scheduling a new reminder
            task_from_db.last_notified = None
            task_from_db.reminder_sent = False
            session.add(task_from_db)
            session.commit()
            return True
        return False
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error scheduling reminder: {e}")
        if own_session:
            session.rollback()
        return False
    finally:
        if own_session:
            session.close()


def validate_reminder_conflicts(task_id: int, reminder_time: datetime, session: Session = None) -> bool:
    """
    Check for potential conflicts with existing reminders

    Args:
        task_id: The ID of the task to schedule a reminder for
        reminder_time: The proposed reminder time
        session: Database session (will be created if not provided)

    Returns:
        bool: True if no conflicts, False otherwise
    """
    own_session = False
    if session is None:
        session = Session(engine)
        own_session = True

    try:
        # Check if there's already a reminder scheduled for this task at this time
        task = session.get(Task, task_id)
        if task and task.reminder_at and task.reminder_at == reminder_time:
            return False  # Conflict: same time already scheduled

        # Additional conflict checks can be added here if needed
        # For example, checking if there are too many reminders in a short time period

        return True
    except Exception:
        return False
    finally:
        if own_session:
            session.close()


def validate_reminder_time(reminder_time: datetime) -> bool:
    """
    Validate that the reminder time is reasonable

    Args:
        reminder_time: The proposed reminder time

    Returns:
        bool: True if valid, False otherwise
    """
    now = datetime.utcnow()

    # Check if the reminder time is not too far in the future (e.g., more than 1 year)
    max_duration = timedelta(days=365)
    if (reminder_time - now) > max_duration:
        return False

    # Check if the reminder time is not in the past
    if reminder_time < now:
        return False

    return True