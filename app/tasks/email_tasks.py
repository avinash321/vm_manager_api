from app.core.celery_worker_app import celery_app
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, email, vm_name):
    logger.info(f"Email task started for {email}, VM: {vm_name}")
    
    try:
        sender_email = os.getenv("EMAIL_USER")
        app_password = os.getenv("EMAIL_PASS")

        if not sender_email or not app_password:
            logger.warning("Email credentials are missing in environment variables")

        subject = "VM Created Successfully"
        body = f"""
                <html>
                <body>
                    <h2 style="color:green;">✅ VM Created Successfully</h2>
                    <p>Your VM <b>{vm_name}</b> is ready.</p>
                    <p>Thanks,<br>VM Manager Team</p>
                </body>
                </html>
                """

        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "html"))
        logger.info("Email message constructed successfully")

        # Connect to Gmail SMTP
        logger.info("Connecting to Gmail SMTP server")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        server.starttls()
        logger.info("Started TLS session")

        server.login(sender_email, app_password)
        logger.info("Logged in to SMTP server successfully")

        # Send email
        server.send_message(msg)
        logger.info(f"Sending email to {email} .....")
        time.sleep(2)
        logger.info(f"Email sent successfully to {email}")

        server.quit()
        logger.info("SMTP connection closed")

        print("✅ Email sent successfully!")

    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        logger.info(f"Retrying email for {email} in 5 seconds (Attempt {self.request.retries + 1})")
        
        print("❌ Error sending email, retrying...")
        raise self.retry(exc=e, countdown=5)