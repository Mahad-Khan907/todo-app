"""
Email service for sending reminder notifications to users
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
from datetime import datetime
from sqlmodel import Session
from ..models import User, Task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    """Service class for handling email notifications"""

    @staticmethod
    def get_smtp_config():
        """Get SMTP configuration from environment variables"""
        password = os.getenv('SMTP_PASSWORD', '')
        # Remove all whitespace from password (common with Gmail 16-character App Passwords)
        clean_password = password.replace(' ', '').strip() if password else password

        config = {
            'smtp_host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'smtp_user': os.getenv('SMTP_USER'),
            'smtp_password': clean_password,
        }

        return config

    @staticmethod
    def send_reminder_email(
        user_email: str, 
        task_title: str, 
        task_description: Optional[str] = None,
        priority: Optional[str] = 'medium',
        due_date: Optional[str] = None
    ):
        """
        Send a polished, high-end HTML email reminder to the user.
        """
        try:
            config = EmailService.get_smtp_config()

            if not config['smtp_user'] or not config['smtp_password']:
                logger.warning("SMTP user or password not configured, skipping email notification")
                return False

            logger.info(f"Dispatching reminder email to logged-in user: {user_email}")

            msg = MIMEMultipart('alternative')
            msg['From'] = f"TaskFlow AI <{config['smtp_user']}>"
            msg['To'] = user_email
            msg['Subject'] = f"⏰ Task Reminder: {task_title}"

            clean_desc = task_description or "No additional description provided."
            priority_color = "#ef4444" if priority == "high" else "#f59e0b" if priority == "medium" else "#10b981"
            priority_label = (priority or "normal").upper()

            # Plain text fallback
            plain_text = f"""Task Reminder: {task_title}
Priority: {priority_label}
Description: {clean_desc}

Stay focused and get it done!
- TaskFlow AI Reminder System
"""

            # Premium HTML Email Template
            html_body = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Task Reminder</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #e2e8f0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f17; padding: 40px 20px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" max-width="560px" style="max-width: 560px; background-color: #111827; border: 1px solid #1f2937; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); padding: 28px 32px; text-align: left;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td>
                    <span style="display: inline-block; background-color: rgba(255, 255, 255, 0.2); padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #ffffff; text-transform: uppercase;">
                      ⚡ TaskFlow Notification
                    </span>
                    <h1 style="margin: 10px 0 0 0; font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">
                      Scheduled Reminder
                    </h1>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Content Body -->
          <tr>
            <td style="padding: 32px;">
              <p style="margin: 0 0 16px 0; font-size: 14px; color: #94a3b8;">
                Hi there, this is your scheduled reminder for the following task:
              </p>

              <!-- Task Card -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #1f2937; border: 1px solid #374151; border-radius: 12px; margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px;">
                    <div style="margin-bottom: 8px;">
                      <span style="display: inline-block; background-color: rgba(255,255,255,0.05); border: 1px solid {priority_color}; color: {priority_color}; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 6px; letter-spacing: 0.5px;">
                        {priority_label} PRIORITY
                      </span>
                    </div>
                    <h2 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700; color: #f8fafc; line-height: 1.3;">
                      {task_title}
                    </h2>
                    <p style="margin: 0; font-size: 13px; color: #cbd5e1; line-height: 1.5;">
                      {clean_desc}
                    </p>
                  </td>
                </tr>
              </table>

              <!-- Call to Action -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="http://localhost:3001/dashboard" style="display: inline-block; background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%); color: #ffffff; font-size: 14px; font-weight: 700; text-decoration: none; padding: 12px 28px; border-radius: 10px; box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);">
                      Open Workspace Dashboard &rarr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #0f172a; border-top: 1px solid #1e293b; padding: 20px 32px; text-align: center;">
              <p style="margin: 0; font-size: 11px; color: #64748b;">
                Sent automatically by <strong>TaskFlow AI</strong> to your registered account.<br>
                Keep building and achieving your goals.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

            msg.attach(MIMEText(plain_text, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))

            server = smtplib.SMTP(config['smtp_host'], config['smtp_port'])
            server.starttls()
            server.login(config['smtp_user'], config['smtp_password'])
            server.sendmail(config['smtp_user'], user_email, msg.as_string())
            server.quit()

            logger.info(f"HTML Reminder email successfully delivered to user {user_email} for task '{task_title}'")
            return True

        except Exception as e:
            logger.error(f"Error sending reminder email to {user_email}: {e}")
            return False

    @staticmethod
    def process_due_reminders(session: Session):
        """
        Process all due reminders and send notification emails to the owning user
        """
        try:
            now = datetime.utcnow()
            from sqlalchemy import and_
            from ..models import Task

            tasks_to_notify = session.query(Task).filter(
                and_(
                    Task.reminder_at != None,
                    Task.reminder_at <= now,
                    Task.reminder_sent == False
                )
            ).all()

            processed_count = 0
            for task in tasks_to_notify:
                user = session.get(User, task.user_id)
                if user and user.email:
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
                        session.commit()
                        processed_count += 1
                else:
                    logger.error(f"Could not find owner user for task {task.id}")

            return processed_count
        except Exception as e:
            logger.error(f"Error processing due reminders: {e}")
            return 0
