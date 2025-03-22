from typing import Callable

from services.email import EmailService


def get_email_service_factory() -> Callable[[], EmailService]:
    return lambda: EmailService()
