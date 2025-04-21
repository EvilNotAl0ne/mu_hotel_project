import os
import django

# Настройка Django
def setup_django():
    """
    Устанавливает настройки Django для работы с проектом.
    Это необходимо для использования моделей и других компонентов Django.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_project.settings')
    django.setup()

# Импорт бота
def import_bot():
    """
    Импортирует экземпляр Telegram-бота из модуля handlers.
    """
    from bot.handlers import bot
    return bot

if __name__ == "__main__":
    try:
        # Настройка Django
        setup_django()

        # Импорт и запуск бота
        bot = import_bot()
        print("Бот запущен. Ожидание сообщений...")
        bot.polling(none_stop=True)  # Запуск бота в режиме постоянного опроса
    except KeyboardInterrupt:
        print("Бот остановлен пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")