# bot/__init__.py
from .handlers import bot

def run_bot():
    print("Бот запущен...")
    bot.polling()