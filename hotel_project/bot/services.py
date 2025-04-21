
from django.core.mail import send_mail

def send_cancellation_email(email, booking_id):
    cancellation_link = f"http://yourdomain.com/cancel/{booking_id}/"
    send_mail(
        "Отмена бронирования",
        f"Чтобы отменить бронирование, перейдите по ссылке: {cancellation_link}",
        "noreply@yourdomain.com",
        [email],
        fail_silently=False,
    )