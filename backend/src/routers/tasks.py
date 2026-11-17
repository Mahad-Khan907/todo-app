from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic, User
from ..database import get_session
from ..auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskPublic])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user.

    Args:
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        List of tasks belonging to the current user
    """
    tasks = session.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.post("/", response_model=TaskPublic)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user.

    Args:
        task_create: Task creation data
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        The created task
    """
    from ..services.task_service import TaskService
    from datetime import datetime

    # Validate recurring task data if applicable
    if task_create.is_recurring:
        TaskService.validate_recurring_task_data(task_create.is_recurring, task_create.recurring_pattern)

    task = Task(
        **task_create.dict(exclude_unset=True),
        user_id=current_user.id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    # If a reminder is set, schedule it
    if task_create.reminder_at:
        try:
            # Handle timezone-aware datetime comparison
            from datetime import timezone
            now_utc = datetime.now(timezone.utc)

            # Ensure reminder_at is timezone-aware for comparison
            reminder_time = task_create.reminder_at
            if reminder_time.tzinfo is None:
                # Assume UTC if no timezone info
                from datetime import timezone
                reminder_time = reminder_time.replace(tzinfo=timezone.utc)

            # Validate reminder time is in the future
            if reminder_time > now_utc:
                # Schedule the reminder
                from ..utils.reminders import schedule_reminder
                success = schedule_reminder(task, reminder_time, session)
                if not success:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to schedule reminder for task {task.id}")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error scheduling reminder for task {task.id}: {e}")

    return task


@router.post("/recurring", response_model=TaskPublic)
async def create_recurring_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new recurring task for the current user.

    Args:
        task_create: Recurring task creation data
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        The created recurring task

    Raises:
        HTTPException: If recurring task data is invalid
    """
    from ..services.task_service import TaskService
    from datetime import datetime

    # Ensure this is a recurring task
    if not task_create.is_recurring:
        task_create.is_recurring = True

    # Validate recurring task data
    TaskService.validate_recurring_task_data(task_create.is_recurring, task_create.recurring_pattern)

    task = Task(
        **task_create.dict(exclude_unset=True),
        user_id=current_user.id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    # If a reminder is set, schedule it
    if task_create.reminder_at:
        try:
            # Handle timezone-aware datetime comparison
            from datetime import timezone
            now_utc = datetime.now(timezone.utc)

            # Ensure reminder_at is timezone-aware for comparison
            reminder_time = task_create.reminder_at
            if reminder_time.tzinfo is None:
                # Assume UTC if no timezone info
                reminder_time = reminder_time.replace(tzinfo=timezone.utc)

            # Validate reminder time is in the future
            if reminder_time > now_utc:
                # Schedule the reminder
                from ..utils.reminders import schedule_reminder
                success = schedule_reminder(task, reminder_time, session)
                if not success:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to schedule reminder for recurring task {task.id}")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error scheduling reminder for recurring task {task.id}: {e}")

    return task


@router.get("/recurring/{task_id}", response_model=TaskPublic)
async def get_recurring_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve information about a specific recurring task.

    Args:
        task_id: The ID of the recurring task to retrieve
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        The recurring task information

    Raises:
        HTTPException: If task doesn't exist, doesn't belong to user, or is not recurring
    """
    # Ensure task_id is an integer if the table uses integer IDs
    try:
        int_id = int(task_id)
        task = session.get(Task, int_id)
    except (ValueError, TypeError):
        task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current user
    if str(task.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    # Verify that this is indeed a recurring task
    if not task.is_recurring:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is not a recurring task"
        )

    return task


@router.get("/{task_id}", response_model=TaskPublic)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Args:
        task_id: The ID of the task to retrieve
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        The requested task if it belongs to the current user

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to the user
    """
    # Ensure task_id is an integer if the table uses integer IDs
    try:
        int_id = int(task_id)
        task = session.get(Task, int_id)
    except (ValueError, TypeError):
        task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current_user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.patch("/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.

    Args:
        task_id: The ID of the task to update
        task_update: Task update data
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        The updated task

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to the user
    """
    from ..services.task_service import TaskService

    # Ensure task_id is an integer if the table uses integer IDs
    try:
        int_id = int(task_id)
        task = session.get(Task, int_id)
    except (ValueError, TypeError):
        task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check if task belongs to current_user before updating
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Store original completion status to detect changes
    original_completed = task.completed
    original_is_recurring = task.is_recurring
    original_recurring_pattern = task.recurring_pattern

    update_data = task_update.dict(exclude_unset=True)
    time_field_changed = False

    for field, value in update_data.items():
        if field == "completed" and value is True and task.completed is False:
            task.completed_at = datetime.utcnow()
        elif field == "completed" and value is False and task.completed is True:
            task.completed_at = None
        elif field in ["reminder_at", "due_date"] and value is not None:
            # When time-related fields change, reset scheduler flags to refresh internal state
            task.reminder_sent = False  # Reset is_notified
            task.last_notified = None   # Reset last_processed_at
            time_field_changed = True
        setattr(task, field, value)

    # If time fields changed, this ensures the scheduler will re-evaluate the task
    # The scheduler will now recognize this task as needing processing again

    # Special handling when a recurring task is marked as completed
    # COMMENTED OUT: Do not create new tasks when any task is marked as complete
    # new_task_instance = None
    # if (original_completed is False and task.completed is True and
    #     original_is_recurring and original_recurring_pattern):
    #     # Create the next occurrence of the recurring task
    #     new_task_instance = TaskService.handle_completed_recurring_task(task, session)

    session.add(task)
    session.commit()
    session.refresh(task)

    # If a new recurring task was created, return both the completed task and the new one
    # For API compatibility, we'll return the updated original task
    # The new task will be available separately in the database
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.

    Args:
        task_id: The ID of the task to delete
        current_user: The authenticated user (from JWT token)
        session: Database session dependency

    Returns:
        Success message

    Raises:
        HTTPException: If task doesn't exist or doesn't belong to the user
    """
    # Ensure task_id is an integer if the table uses integer IDs
    try:
        int_id = int(task_id)
        task = session.get(Task, int_id)
    except (ValueError, TypeError):
        task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check ownership before deletion
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}