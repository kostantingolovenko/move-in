import time
from celery import Celery
import random

celery_app = Celery(
    "movein_tasks",
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def send_verification_email(user_email: str):
    print(f"[CELERY WORKER] Надсилаємо лист на пошту {user_email}...")

    time.sleep(5)

    print(f"[CELERY WORKER] Лист для верефікації надіслано на {user_email}!")
    return {"status": "Success", "sent_to": user_email}

@celery_app.task(bind=True, max_retries=3)
def send_sms_reminder(self, phone_number: str):
    sms_gateway_chance = random.randint(1, 10)

    try:
        if sms_gateway_chance <= 5:
            raise Exception("СМС-шлюз не відповідає!")
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)

    print("SMS успішно надіслано")