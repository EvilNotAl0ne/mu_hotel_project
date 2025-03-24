from django.contrib.messages.context_processors import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Отправляет электронное письмо пользователю с инструкцией по отмене бронирования
def send_cancel_email(booking):
    # Генерируем URL для страницы подтверждения
    cancel_url = reverse('cancel_booking_by_token', args=[booking.cancel_token])
    full_url = f"http://127.0.0.1:8000{cancel_url}"

    # Формируем сообщение
    message = f"Для отмены бронирования перейдите по ссылке: {full_url}"
    print(message)  # Чисто для тестов выводим в терминал