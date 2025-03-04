from pydantic import BaseModel

from celery.app import Celery

from .environs import REDIS_URL, BASE_URL

celery_app = Celery("celery", broker=REDIS_URL, backend=REDIS_URL)

class TaskStatus(BaseModel):
    id: str
    status: str

@celery_app.task(name="tasks.print_user_data")
def print_user_data(user: dict) -> bool:
    for key, value in user.items():
        print(f"{key}: {value}")
    return True