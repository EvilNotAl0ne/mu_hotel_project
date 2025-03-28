# Generated by Django 5.1.7 on 2025-03-23 20:32

from django.db import migrations
from django.db import migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_booking_cancel_token'),
    ]

    operations = [
    ]


def generate_unique_tokens(apps, schema_editor):
    Booking = apps.get_model('main', 'Booking')  # Замените 'main' на имя вашего приложения
    for booking in Booking.objects.all():
        if not booking.cancel_token:  # Если токен пустой
            booking.cancel_token = str(uuid.uuid4())
            booking.save()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_booking_cancel_token'),  # Замените на имя предыдущей миграции
    ]

    operations = [
        migrations.RunPython(generate_unique_tokens),
    ]