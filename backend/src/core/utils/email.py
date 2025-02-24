import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config.config import settings


async def send_verification_email(email: str, token: str):
    sender = settings.email_settings.SMTP_USER
    password = settings.email_settings.SMTP_PASSWORD

    server = smtplib.SMTP_SSL(settings.email_settings.SMTP_HOST, settings.email_settings.SMTP_PORT)
    server.login(sender, password)

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = 'Подтверждение email'

    verification_link = f"{settings.api_settings.BASE_URL}/api/v1/users/verify/{token}"
    body = f"Для подтверждения email перейдите по ссылке: {verification_link}"
    msg.attach(MIMEText(body, 'plain'))

    server.send_message(msg)
    server.quit()
