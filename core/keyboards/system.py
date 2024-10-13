from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State


class FormStates(StatesGroup):
    waiting_for_response = State()
    waiting_for_response_dop = State()


def keyboard_system():
    button1 = types.KeyboardButton(text="📸 Скриншот")
    button2 = types.KeyboardButton(text="📹 Запись (10 секунд)")
    button3 = types.KeyboardButton(text="⏹ Главное меню")
    button4 = types.KeyboardButton(text="❌ Блокировка ПК")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Жду команду")
    keyboard.add(button1, button2)
    keyboard.add(button4)
    keyboard.row(button3)
    return keyboard
