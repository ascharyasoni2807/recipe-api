from celery import shared_task
from django.conf import settings
from .models import Recipe
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import traceback

logger = logging.getLogger("recipe")

def send_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        logger.info(f'Email sent successfully by {from_email} to {to_email} ')
    except Exception as e:
        logger.error(f"Failed to send email: {e}", exc_info=True)
    finally:
        server.quit()

@shared_task
def send_email_task(subject, message, recipient_id):
    send_email(
        subject=subject,
        body=message,
        to_email=recipient_id,
        from_email=settings.EMAIL_HOST_USER,
        smtp_server=settings.EMAIL_HOST,
        smtp_port=settings.EMAIL_PORT,
        smtp_user=settings.EMAIL_HOST_USER,
        smtp_password=settings.EMAIL_HOST_PASSWORD
    )

@shared_task
def send_daily_notifications():
    recipes = Recipe.objects.all()
    logger.info(f"Objects are {recipes}")
    for recipe in recipes:
        author = recipe.author
        likes = recipe.get_total_number_of_likes()
        logger.info(f"Likes are {likes}")
        if likes > 0:
            subject = 'Daily Recipe Likes Notification'
            message = f'Your recipe {recipe.title} has received new {likes} likes today.'
            send_email_task.delay(subject, message, author.email)
