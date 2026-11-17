"""
Task service for handling recurring task logic and other task operations
"""
from datetime import datetime, timedelta
from sqlmodel import Session, select
from typing import Optional
import logging
from ..models import Task, TaskUpdate
from ..utils.recurring_tasks import calculate_next_occurrence

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskService:
    """Service class for handling task operations"""

    @staticmethod
    def handle_completed_recurring_task(task: Task, session: Session) -> Optional[Task]:
        """
        Handle a completed recurring task by creating the next occurrence

        Args:
            task: The completed recurring task
            session: Database session

        Returns:
            The newly created task instance or None if not recurring
        """
        try:
            if not task.is_recurring or not task.recurring_pattern:
                return None

            # Calculate next occurrence date
            next_occurrence = calculate_next_occurrence(task)

            # Create new task instance with same properties
            new_task = Task(
                title=task.title,
                description=task.description,
                completed=False,
                priority=task.priority,
                due_date=next_occurrence,
                completed_at=None,
                is_recurring=task.is_recurring,
                recurring_pattern=task.recurring_pattern,
                recurrence_id=task.recurrence_id or str(task.id),  # Link to the same recurring series
                reminder_at=task.reminder_at,  # Carry over reminder settings if any
                last_notified=None,
                reminder_sent=False,  # New task hasn't had its reminder sent yet
                user_id=task.user_id,
                tags=task.tags.copy() if task.tags else []
            )

            # Add the new task to the session
            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return new_task
        except Exception as e:
            logger.error(f"Error handling completed recurring task: {e}")
            logger.exception("Full traceback:")
            session.rollback()
            return None

    @staticmethod
    def update_task_with_validation(task_id: int, task_update: TaskUpdate, session: Session, user_id: str) -> Optional[Task]:
        """
        Update a task with validation and special handling for recurring tasks

        Args:
            task_id: ID of the task to update
            task_update: Update data
            session: Database session
            user_id: ID of the user making the update

        Returns:
            Updated task or None if not found
        """
        from ..models import Task  # Import here to avoid circular imports
        task = session.get(Task, task_id)

        if not task:
            return None

        # Verify ownership
        if str(task.user_id) != user_id:
            raise PermissionError("Not authorized to update this task")

        # Store original completion status to detect changes
        original_completed = task.completed
        original_is_recurring = task.is_recurring
        original_recurring_pattern = task.recurring_pattern

        # Apply updates
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)

        # Special handling when a recurring task is marked as completed
        new_task_instance = None
        if (original_completed is False and task.completed is True and
            original_is_recurring and original_recurring_pattern):
            # Create the next occurrence of the recurring task
            new_task_instance = TaskService.handle_completed_recurring_task(task, session)

        session.add(task)
        session.commit()
        session.refresh(task)

        # Return the new task instance if created
        return task, new_task_instance

    @staticmethod
    def calculate_next_occurrence(task: Task, last_completion_date: Optional[datetime] = None) -> datetime:
        """
        Calculate the next occurrence for a recurring task

        Args:
            task: The recurring task
            last_completion_date: The date when the task was last completed

        Returns:
            datetime: The next occurrence date
        """
        from ..utils.recurring_tasks import calculate_next_occurrence as calc_func
        return calc_func(task, last_completion_date)

    @staticmethod
    def validate_recurring_task_data(is_recurring: bool, recurring_pattern: Optional[str]) -> bool:
        """
        Validate recurring task data

        Args:
            is_recurring: Whether the task is recurring
            recurring_pattern: The recurring pattern

        Returns:
            bool: True if valid, raises exception if invalid
        """
        if is_recurring:
            if not recurring_pattern:
                raise ValueError("Recurring tasks must have a pattern specified")

            valid_patterns = ["daily", "weekly", "monthly", "custom"]
            if recurring_pattern not in valid_patterns:
                raise ValueError(f"Invalid recurring pattern: {recurring_pattern}. Must be one of {valid_patterns}")

        return True