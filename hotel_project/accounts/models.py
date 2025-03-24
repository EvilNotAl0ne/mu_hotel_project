from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Определяем модель для профиля
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # user - это модель нашего юзера, on_delete=models.CASCADE - это параметр при случаи удаления юзера и удалялся его профиль
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    phone_number =models.CharField(max_length=14, blank=True, verbose_name='Номер телефона')
    passport_data = models.CharField(max_length=50, blank=True, verbose_name='Паспортные данные')

def __str__(self):
    return f"{self.user.username} Profile"

# Определяем сигнал для нашей модели Profile
# Декоратор связывает нашу функцию с сигналом (post_save) что бы автоматически создавался профиль при регистрации юзера
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# Также связывает, только сохраняет изменения в профиле
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()