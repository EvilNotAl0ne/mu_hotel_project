# Generated by Django 5.1.7 on 2025-03-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_booking_cancel_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
