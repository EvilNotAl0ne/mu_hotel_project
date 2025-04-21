import requests
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from .keyboards import get_main_menu, get_main_menu_button

# Глобальные переменные
BOT_TOKEN = "7939429240:AAEKhK8j3xc-cBAU8pc1ifDX1xNwSRPo0gw"
API_URL = "http://127.0.0.1:8000/api/"
bot = TeleBot(BOT_TOKEN)
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я помогу вам забронировать номер в отеле.",
        reply_markup=get_main_menu()
    )

# Обработчик кнопки "На главную"
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def return_to_main_menu(call):
    bot.send_message(
        call.message.chat.id,
        "Вы вернулись в главное меню.",
        reply_markup=get_main_menu()
    )

# Кнопка "Подобрать номер"
@bot.message_handler(func=lambda message: message.text == "Подобрать номер")
def find_room(message):
    markup = get_main_menu_button()
    bot.send_message(
        message.chat.id,
        "На какую дату желаете забронировать? Введите даты в формате: 'YYYY-MM-DD - YYYY-MM-DD'",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, process_dates)

# Обработка ввода дат
def process_dates(message):
    try:
        date_parts = message.text.split(" - ")
        if len(date_parts) != 2:
            bot.reply_to(message, "Неверный формат дат. Введите даты в формате: 'YYYY-MM-DD - YYYY-MM-DD'")
            return
        check_in, check_out = date_parts[0].strip(), date_parts[1].strip()
        chat_id = message.chat.id
        user_data[chat_id] = {"check_in": check_in, "check_out": check_out}

        response = requests.get(f"{API_URL}room-categories/")
        categories = response.json()
        if not categories:
            bot.reply_to(message, "Нет доступных категорий комнат.")
            return

        category_message = "Выберите категорию комнаты:\n"
        for category in categories:
            category_message += f"ID: {category['id']}\n"
            category_message += f"✨ Название: {category['name']}\n"
            category_message += f"📝 Описание: {category['description'] or 'Отсутствует'}\n"

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("Назад", callback_data="find_room"),
            InlineKeyboardButton("На главную", callback_data="main_menu")
        )

        bot.send_message(
            message.chat.id,
            category_message,
            reply_markup=markup
        )
        bot.send_message(
            message.chat.id,
            "Введите ID подходящей вам категории:"
        )
        bot.register_next_step_handler(message, process_category_selection)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработка выбора категории
def process_category_selection(message):
    try:
        chat_id = message.chat.id
        user_info = user_data.get(chat_id, {})
        check_in = user_info.get("check_in")
        check_out = user_info.get("check_out")

        if not check_in or not check_out:
            bot.reply_to(message, "Не указаны даты заезда или выезда. Пожалуйста, начните заново.")
            return

        category_id = int(message.text.strip())
        response = requests.get(
            f"{API_URL}rooms/",
            params={"category": category_id, "check_in": check_in, "check_out": check_out}
        )
        rooms = response.json()

        for room in rooms:
            room_info = (
                f"ID: {room['id']}\n"
                f"Название: {room['name']}\n"
                f"Цена за ночь: {room['price_per_night']} руб.\n"
                f"Описание: {room['description'] or 'Отсутствует'}\n"
            )
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton("Забронировать", callback_data=f"book_{room['id']}"),
                InlineKeyboardButton("Назад", callback_data="select_category"),
                InlineKeyboardButton("На главную", callback_data="main_menu")
            )
            bot.send_message(
                message.chat.id,
                room_info,
                reply_markup=markup
            )
    except ValueError:
        bot.reply_to(message, "Неверный формат ID категории. Введите число.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработка кнопки "Забронировать"
@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def handle_booking(call):
    try:
        room_id = int(call.data.split("_")[1])
        chat_id = call.message.chat.id
        if chat_id not in user_data:
            user_data[chat_id] = {}
        user_data[chat_id]["room_id"] = room_id

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("Назад", callback_data="select_room"),
            InlineKeyboardButton("На главную", callback_data="main_menu")
        )

        bot.send_message(
            call.message.chat.id,
            "Введите данные для бронирования в формате: first_name, last_name, email, phone",
            reply_markup=markup
        )
        bot.register_next_step_handler(call.message, process_booking)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")

# Обработка данных для бронирования
def process_booking(message):
    try:
        chat_id = message.chat.id
        data_parts = message.text.split(",")
        if len(data_parts) != 4:
            bot.reply_to(message, "Неверный формат данных. Введите данные в формате: first_name, last_name, email, phone")
            return

        first_name = data_parts[0].strip()
        last_name = data_parts[1].strip()
        email = data_parts[2].strip()
        phone = data_parts[3].strip()

        from accounts.models import Profile
        profile, created = Profile.objects.get_or_create(chat_id=chat_id)
        profile.update_from_telegram(
            chat_id=chat_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )

        booking_data = {
            "room": user_data[chat_id]["room_id"],
            "check_in": user_data[chat_id]["check_in"],
            "check_out": user_data[chat_id]["check_out"],
            "guests": 1,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
        }

        response = requests.post(f"{API_URL}bookings/", json=booking_data)
        if response.status_code == 201:
            bot.send_message(chat_id, "Номер успешно забронирован!")
        else:
            error_message = response.json().get("detail", "Неизвестная ошибка")
            bot.send_message(chat_id, f"Ошибка при бронировании: {error_message}")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработка кнопки "Мои бронирования"
@bot.message_handler(func=lambda message: message.text == "Мои бронирования")
def handle_my_bookings(message):
    show_my_bookings(message)

# Показать мои бронирования
@bot.message_handler(commands=['my_bookings'])
def show_my_bookings(message):
    try:
        chat_id = message.chat.id
        from accounts.models import Profile
        profile = Profile.objects.filter(chat_id=chat_id).first()

        if not profile or not profile.telegram_email:
            bot.reply_to(message, "Вы еще не зарегистрированы. Введите данные для бронирования.")
            return

        email = profile.telegram_email
        response = requests.get(f"{API_URL}bookings/", params={"email": email})
        if response.status_code != 200:
            bot.reply_to(message, "Ошибка при получении бронирований.")
            return

        bookings = response.json()
        if not isinstance(bookings, list) or not bookings:
            bot.reply_to(message, "У вас нет активных бронирований.")
            return

        booking_message = "Ваши бронирования:\n"
        markup = InlineKeyboardMarkup()
        for booking in bookings:
            room_info = booking['room']
            room_name = room_info['name'] if isinstance(room_info, dict) else str(room_info)
            booking_message += (
                f"ID: {booking['id']}\n"
                f"Номер: {room_name}\n"
                f"Даты: {booking['check_in']} - {booking['check_out']}\n"
                f"Имя: {booking['first_name']}\n"
                f"Фамилия: {booking['last_name']}\n"
                f"Email: {booking['email']}\n"
                f"Телефон: {booking['phone']}\n"
            )
            markup.add(InlineKeyboardButton(f"Отменить ID: {booking['id']}", callback_data=f"cancel_{booking['id']}"))

        bot.send_message(message.chat.id, booking_message, reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Отмена бронирования
@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_"))
def handle_cancel_booking(call):
    try:
        booking_id = call.data.split("_")[1]
        chat_id = call.message.chat.id
        response = requests.delete(f"{API_URL}bookings/{booking_id}/")
        if response.status_code == 204:
            bot.send_message(chat_id, f"Бронирование с ID {booking_id} успешно отменено.")
        else:
            error_message = response.json().get("detail", "Неизвестная ошибка")
            bot.send_message(chat_id, f"Ошибка при отмене бронирования: {error_message}")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {e}")

# Обработчики для кнопок "Назад"
@bot.callback_query_handler(func=lambda call: call.data == "find_room")
def go_back_to_find_room(call):
    find_room(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "select_category")
def go_back_to_category_selection(call):
    bot.send_message(
        call.message.chat.id,
        "Введите ID подходящей вам категории:"
    )
    bot.register_next_step_handler(call.message, process_category_selection)

@bot.callback_query_handler(func=lambda call: call.data == "select_room")
def go_back_to_room_selection(call):
    chat_id = call.message.chat.id
    user_info = user_data.get(chat_id, {})
    category_id = user_info.get("category_id")

    response = requests.get(
        f"{API_URL}rooms/",
        params={"category": category_id, "check_in": user_info["check_in"], "check_out": user_info["check_out"]}
    )
    rooms = response.json()

    for room in rooms:
        room_info = (
            f"ID: {room['id']}\n"
            f"Название: {room['name']}\n"
            f"Цена за ночь: {room['price_per_night']} руб.\n"
            f"Описание: {room['description'] or 'Отсутствует'}\n"
        )
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("Забронировать", callback_data=f"book_{room['id']}"),
            InlineKeyboardButton("Назад", callback_data="select_category"),
            InlineKeyboardButton("На главную", callback_data="main_menu")
        )
        bot.send_message(
            call.message.chat.id,
            room_info,
            reply_markup=markup
        )

# Обработчик кнопки "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль")
def show_profile(message):
    try:
        bot.reply_to(message, "Ваш профиль будет показан здесь.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")