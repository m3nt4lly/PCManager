from aiogram import types


def keyboard_cmd():
    button1 = types.KeyboardButton(text="✒ Выполнить команду")
    button2 = types.KeyboardButton(text="✔ Открыть консоль")
    button3 = types.KeyboardButton(text="❌ Закрыть консоль")
    button4 = types.KeyboardButton(text="⏹ Главное меню")
    button5 = types.KeyboardButton(text="✒ Выполнить команду (Консоль открыта)")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Жду команду")
    keyboard.row(button1)
    keyboard.row(button5)
    keyboard.add(button2, button3)
    keyboard.row(button4)
    return keyboard
