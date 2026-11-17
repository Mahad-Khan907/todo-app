"""
Background scheduler for recurring tasks and reminders
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from .models import Task, User
from .database import engine
import logging
from .services.email_service import EmailService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        """Start the scheduler with recurring tasks and reminder jobs"""
        self.scheduler.add_job(
            self.process_recurring_tasks,
            IntervalTrigger(seconds=30),
            id='process_recurring_tasks',
            name='Process recurring tasks',
            replace_existing=True,
            misfire_grace_time=60,
            coalesce=True
        )

        self.scheduler.add_job(
            self.process_reminders,
            IntervalTrigger(seconds=15),  # Check every 15 seconds for timely delivery
            id='process_reminders',
            name='Process reminders',
            replace_existing=True,
            misfire_grace_time=60,
            coalesce=True
        )

        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()

    async def process_recurring_tasks(self):
        """Process recurring tasks to schedule their next occurrences"""
        try:
            with Session(engine) as session:
                completed_recurring_tasks = session.exec(
                    select(Task).where(
                        Task.is_recurring == True,
                        Task.completed == True
                    )
                ).all()

                for task in completed_recurring_tasks:
                    next_due_date = self._calculate_next_date(task)
                    search_recurrence_id = task.recurrence_id or str(task.id)
                    tolerance = timedelta(minutes=1)
                    min_due_date = next_due_date - tolerance
                    max_due_date = next_due_date + tolerance

                    existing_task = session.exec(
                        select(Task).where(
                            Task.recurrence_id == search_recurrence_id,
                            Task.title == task.title,
                            Task.due_date >= min_due_date,
                            Task.due_date <= max_due_date
                        )
                    ).first()

                    if not existing_task:
                        next_task = self._create_next_task_instance(task)
                        if next_task:
                            now = datetime.now(timezone.utc)
                            if next_task.due_date and next_task.due_date > now:
                                session.add(next_task)
                                session.commit()
                                logger.info(f"Created next instance for recurring task: {task.title}")

        except Exception as e:
            logger.error(f"Error processing recurring tasks: {e}")

    def _create_next_task_instance(self, completed_task: Task):
        """Create the next instance of a recurring task"""
        next_due_date = self._calculate_next_date(completed_task)
        next_reminder_at = None

        if completed_task.reminder_at:
            if completed_task.due_date:
                orig_reminder = completed_task.reminder_at
                orig_due = completed_task.due_date
                if orig_reminder.tzinfo is None:
                    orig_reminder = orig_reminder.replace(tzinfo=timezone.utc)
                if orig_due.tzinfo is None:
                    orig_due = orig_due.replace(tzinfo=timezone.utc)

                time_diff = orig_reminder - orig_due
                next_reminder_at = next_due_date + time_diff
            else:
                orig_reminder = completed_task.reminder_at
                if orig_reminder.tzinfo is None:
                    orig_reminder = orig_reminder.replace(tzinfo=timezone.utc)

                next_reminder_at = next_due_date.replace(
                    hour=orig_reminder.hour,
                    minute=orig_reminder.minute,
                    second=orig_reminder.second,
                    microsecond=orig_reminder.microsecond
                )

        new_task = Task(
            title=completed_task.title,
            description=completed_task.description,
            completed=False,
            priority=completed_task.priority,
            due_date=next_due_date,
            completed_at=None,
            is_recurring=completed_task.is_recurring,
            recurring_pattern=completed_task.recurring_pattern,
            recurrence_id=completed_task.recurrence_id or str(completed_task.id),
            reminder_at=next_reminder_at,
            last_notified=None,
            reminder_sent=False,
            user_id=completed_task.user_id,
            tags=completed_task.tags
        )
        return new_task

    def _calculate_next_date(self, task: Task) -> datetime:
        """Calculate the next occurrence date based on the recurring pattern"""
        time_to_preserve = task.due_date if task.due_date else datetime.now(timezone.utc)
        current_ref = datetime.now(timezone.utc)

        if task.recurring_pattern == "daily":
            next_date = current_ref.replace(hour=time_to_preserve.hour,
                                          minute=time_to_preserve.minute,
                                          second=time_to_preserve.second,
                                          microsecond=time_to_preserve.microsecond) + timedelta(days=1)
        elif task.recurring_pattern == "weekly":
            next_date = current_ref.replace(hour=time_to_preserve.hour,
                                          minute=time_to_preserve.minute,
                                          second=time_to_preserve.second,
                                          microsecond=time_to_preserve.microsecond) + timedelta(weeks=1)
        elif task.recurring_pattern == "monthly":
            next_date = current_ref.replace(hour=time_to_preserve.hour,
                                          minute=time_to_preserve.minute,
                                          second=time_to_preserve.second,
                                          microsecond=time_to_preserve.microsecond) + timedelta(days=30)
        else:
            next_date = current_ref.replace(hour=time_to_preserve.hour,
                                          minute=time_to_preserve.minute,
                                          second=time_to_preserve.second,
                                          microsecond=time_to_preserve.microsecond) + timedelta(days=1)
        return next_date

    async def process_reminders(self):
        """
        Process tasks that have reached their reminder time.
        Sends email directly to the task owner's registered email address.
        """
        try:
            with Session(engine) as session:
                now = datetime.now(timezone.utc)

                # Fetch all tasks where a reminder is set and has not been sent yet
                tasks_with_reminder = session.exec(
                    select(Task).where(
                        Task.reminder_sent == False,
                        Task.reminder_at != None
                    )
                ).all()

                sent_count = 0
                for task in tasks_with_reminder:
                    rem_time = task.reminder_at
                    if rem_time.tzinfo is None:
                        rem_time = rem_time.replace(tzinfo=timezone.utc)

                    # Trigger reminder if current time is at or past reminder_at
                    if rem_time <= now:
                        # Fetch the task's actual owner (the logged-in user who created the task)
                        user = session.get(User, task.user_id)

                        if user and user.email:
                            logger.info(f"Triggering email reminder to task owner: {user.email} for '{task.title}'")
                            success = EmailService.send_reminder_email(
                                user_email=user.email,
                                task_title=task.title,
                                task_description=task.description,
                                priority=task.priority
                            )

                            if success:
                                task.last_notified = now
                                task.reminder_sent = True
                                session.add(task)
                                sent_count += 1
                                logger.info(f"Marked reminder_sent = True for task {task.id}")
                            else:
                                logger.warning(f"SMTP delivery failed for task {task.id} to {user.email}")
                        else:
                            logger.error(f"User not found for task {task.id} (user_id: {task.user_id})")

                if sent_count > 0:
                    session.commit()
                    logger.info(f"Processed and committed {sent_count} due reminders")

        except Exception as e:
            logger.error(f"Error in process_reminders: {e}")

# Global scheduler instance
task_scheduler = TaskScheduler()
