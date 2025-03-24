import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config.config import settings


class EmailService:
    def __init__(self):
        self.sender = settings.email_settings.SMTP_USER
        self.password = settings.email_settings.SMTP_PASSWORD
        self.base_url = settings.api_settings.BASE_URL

    async def send_verification_email(self, email: str, token: str):
        server = smtplib.SMTP_SSL(
            settings.email_settings.SMTP_HOST, settings.email_settings.SMTP_PORT
        )
        server.login(self.sender, self.password)

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = email
        msg["Subject"] = "Подтверждение email"

        verification_link = f"{self.base_url}/api/v1/users/verify/{token}"
        body = f"Для подтверждения email перейдите по ссылке: {verification_link}"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
        server.quit()

    async def send_change_password_email(self, email: str, token: str):
        server = smtplib.SMTP_SSL(
            settings.email_settings.SMTP_HOST, settings.email_settings.SMTP_PORT
        )
        server.login(self.sender, self.password)

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = email
        msg["Subject"] = "Изменение пароля"

        change_password_link = f"{self.base_url}/api/v1/users/password-reset/{token}"
        body = f"Для изменения пароля перейдите по ссылке: {change_password_link}"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
        server.quit()
