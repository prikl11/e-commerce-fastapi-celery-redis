from typing import Annotated
from fastapi import Depends

from app.services.email import EmailService

def get_email_service() -> EmailService:
    return EmailService()

EmailServiceDep = Annotated[EmailService, Depends(get_email_service)]