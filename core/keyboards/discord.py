from aiogram import types


def keyboard_discord():
    button1 = types.KeyboardButton(text="🟢 Онлайн")
    button2 = types.KeyboardButton(text="🟠 Неактивен")
    button3 = types.KeyboardButton(text="🔴 Не беспокоить")
    button4 = types.KeyboardButton(text="⚪ Невидимка")
    button5 = types.KeyboardButton(text="⏹ Главное меню")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Жду команду")
    keyboard.add(button1, button2, button3, button4)
    keyboard.row(button5)
    return keyboard
