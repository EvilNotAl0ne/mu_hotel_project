from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Модель для хранения дополнительной информации о пользователе.
    Связана с моделью User через OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    phone_number = models.CharField(max_length=14, blank=True, verbose_name='Номер телефона')
    passport_data = models.CharField(max_length=50, blank=True, verbose_name='Паспортные данные')
    chat_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name='Telegram Chat ID')
    telegram_email = models.EmailField(null=True, blank=True, verbose_name='Email для бронирования')

    def __str__(self):
        """
        Возвращает строковое представление профиля.
        """
        return f"{self.user.username} Profile" if self.user else "Profile without User"

    def is_linked_to_telegram(self):
        """
        Проверяет, связан ли профиль с Telegram (наличие chat_id).
        """
        return self.chat_id is not None

    def update_from_telegram(self, chat_id, first_name, last_name, email, phone):
        """
        Обновляет данные профиля из Telegram.
        Если какое-то поле не передано, сохраняет текущее значение.
        """
        self.chat_id = chat_id
        self.first_name = first_name or self.first_name
        self.last_name = last_name or self.last_name
        self.telegram_email = email or self.telegram_email
        self.phone_number = phone or self.phone_number
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создает профиль пользователя автоматически при создании нового User.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль пользователя при сохранении User.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()