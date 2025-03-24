from django.core.mail import send_mail
from django.conf import settings

# Отправляет электронное письмо пользователю с инструкцией по отмене бронирования
def send_cancel_email(booking):
    subject = "Отмена бронирования"
    message = f"Для отмены бронирования перейдите по ссылке: http://127.0.0.1:8000/cancel/{booking.cancel_token}/"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.email] if booking.user else ["guest@example.com"]
    send_mail(subject, message, from_email, recipient_list)