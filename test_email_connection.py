"""
Test script to verify email service connection
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    """Test SMTP connection to Gmail"""

    # Load environment variables
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD', '')

    # Clean password (remove spaces)
    clean_password = smtp_password.replace(' ', '') if smtp_password else smtp_password

    print(f"Testing SMTP connection to: {smtp_host}:{smtp_port}")
    print(f"Using email: {smtp_user}")
    print(f"Password length: {len(clean_password) if clean_password else 0} characters")

    if not smtp_user or not clean_password:
        print("[FAILED] Missing SMTP credentials")
        print("Please check your .env file for SMTP_USER and SMTP_PASSWORD")
        return False

    try:
        print("Attempting to connect to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        print("[SUCCESS] Connected to SMTP server")

        print("Starting TLS encryption...")
        server.starttls()
        print("[SUCCESS] TLS encryption started")

        print("Attempting to login...")
        server.login(smtp_user, clean_password)
        print("[SUCCESS] Login successful")

        # Try to send a test email
        print("Creating test email...")
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = smtp_user  # Send to yourself for testing
        msg['Subject'] = "Test Email from Todo App"

        body = "This is a test email to verify SMTP connection."
        msg.attach(MIMEText(body, 'plain'))

        print("Sending test email...")
        server.sendmail(smtp_user, smtp_user, msg.as_string())
        print("[SUCCESS] Test email sent successfully!")

        server.quit()
        print("[SUCCESS] SMTP connection test completed successfully!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERROR] SMTP Authentication Error: {e}")
        print("This usually means:")
        print("  - Wrong email or password")
        print("  - Need to use App Password instead of regular password")
        print("  - 2-Factor Authentication is not enabled")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"[ERROR] Recipients Refused: {e}")
        return False
    except smtplib.SMTPSenderRefused as e:
        print(f"[ERROR] Sender Refused: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    print("Testing SMTP Connection for Todo App Email Service")
    print("=" * 50)
    success = test_smtp_connection()
    print("=" * 50)
    if success:
        print("[SUCCESS] Email service should work correctly!")
    else:
        print("[FAILED] Email service has issues - please check configuration")