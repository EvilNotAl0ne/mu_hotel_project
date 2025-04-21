from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню с кнопками
def get_main_menu():
    """
    Создает главное меню с кнопками:
    - Подобрать номер
    - Мои бронирования
    - Профиль
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Подобрать номер"))
    markup.add(KeyboardButton("Мои бронирования"))
    markup.add(KeyboardButton("Профиль"))
    return markup

# Кнопка "Забронировать" для комнаты
def get_inline_book_button(room_id):
    """
    Создает inline-кнопку для бронирования конкретного номера.
    :param room_id: ID комнаты
    :return: InlineKeyboardMarkup с кнопкой "Забронировать"
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Забронировать", callback_data=f"book_{room_id}"))
    return markup

# Кнопка "Назад"
def get_back_button(callback_data):
    """
    Создает inline-кнопку "Назад".
    :param callback_data: Действие при нажатии
    :return: InlineKeyboardMarkup с кнопкой "Назад"
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Назад", callback_data=callback_data))
    return markup

# Кнопка "На главную"
def get_main_menu_button():
    """
    Создает inline-кнопку "На главную".
    :return: InlineKeyboardMarkup с кнопкой "На главную"
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("На главную", callback_data="main_menu"))
    return markup