from aiogram import types


def keyboard_main():
    button1 = types.KeyboardButton(text="✉ Discord")
    button2 = types.KeyboardButton(text="🖥 Система")
    button3 = types.KeyboardButton(text="☄ CMD")
    button4 = types.KeyboardButton(text="⚙ Настройки")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Жду команду")
    keyboard.add(button1, button2)
    keyboard.row(button3)
    keyboard.row(button4)
    return keyboard
