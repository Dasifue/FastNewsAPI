import smtplib
from email.mime.text import MIMEText

from pydantic import BaseModel

from celery.app import Celery

from .environs import REDIS_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

celery_app = Celery("celery", broker=REDIS_URL, backend=REDIS_URL)

class TaskStatus(BaseModel):
    id: str
    status: str

@celery_app.task(name="tasks.print_user_data")
def print_user_data(user: dict) -> bool:
    for key, value in user.items():
        print(f"{key}: {value}")
    return True

@celery_app.task(name="tasks.send_verification_code")
def send_verification_code(email: str, code: str) -> bool:
    server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    server.connect(host=SMTP_HOST, port=SMTP_PORT)
    server.starttls()

    try:
        server.login(user=SMTP_USER, password=SMTP_PASSWORD)
        message = MIMEText(code)
        message["Subject"] = "FastNewsAPI email verification"

        server.sendmail(from_addr=SMTP_USER, to_addrs=email, msg=message.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        return False