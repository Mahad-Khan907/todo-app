"""
Utility functions for calculating recurring task occurrences
"""
from datetime import datetime, timedelta
from typing import Optional
from ..models import Task


def calculate_next_occurrence(task: Task, last_completion_date: Optional[datetime] = None) -> datetime:
    """
    Calculate the next occurrence date based on the recurring pattern

    Args:
        task: The recurring task
        last_completion_date: The date when the task was last completed (defaults to now if None)

    Returns:
        datetime: The next occurrence date
    """
    if not task.is_recurring or not task.recurring_pattern:
        raise ValueError("Task is not recurring or has no pattern")

    reference_date = last_completion_date or datetime.utcnow()

    if task.recurring_pattern == "daily":
        return reference_date + timedelta(days=1)
    elif task.recurring_pattern == "weekly":
        return reference_date + timedelta(weeks=1)
    elif task.recurring_pattern == "monthly":
        # For monthly, we'll add approximately one month
        # This is a simplified approach - a more sophisticated one would handle month boundaries
        return reference_date + timedelta(days=30)
    elif task.recurring_pattern == "custom":
        # For custom patterns, we would need to parse the custom pattern
        # For now, default to daily
        return reference_date + timedelta(days=1)
    else:
        # Default to daily if pattern is invalid
        return reference_date + timedelta(days=1)


def get_next_occurrence_for_pattern(pattern: str, reference_date: datetime = None) -> datetime:
    """
    Get the next occurrence based on a pattern string

    Args:
        pattern: The recurring pattern ('daily', 'weekly', 'monthly', 'custom')
        reference_date: The date to calculate from (defaults to now if None)

    Returns:
        datetime: The next occurrence date
    """
    if reference_date is None:
        reference_date = datetime.utcnow()

    if pattern == "daily":
        return reference_date + timedelta(days=1)
    elif pattern == "weekly":
        return reference_date + timedelta(weeks=1)
    elif pattern == "monthly":
        return reference_date + timedelta(days=30)
    elif pattern == "custom":
        # For custom patterns, return the same day next week as a default
        return reference_date + timedelta(weeks=1)
    else:
        raise ValueError(f"Invalid recurring pattern: {pattern}")


def is_recurring_pattern_valid(pattern: str) -> bool:
    """
    Check if a recurring pattern is valid

    Args:
        pattern: The pattern to validate

    Returns:
        bool: True if the pattern is valid, False otherwise
    """
    valid_patterns = ["daily", "weekly", "monthly", "custom"]
    return pattern in valid_patterns


def format_recurring_pattern_display(pattern: str) -> str:
    """
    Format a recurring pattern for display purposes

    Args:
        pattern: The pattern to format

    Returns:
        str: Formatted pattern for display
    """
    pattern_mapping = {
        "daily": "Daily",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "custom": "Custom"
    }

    return pattern_mapping.get(pattern, pattern)