from aiogram import types
from aiogram.dispatcher import FSMContext

from config import telegram_bot_settings


def restricted(func):
    async def wrapped(message: types.Message, state: FSMContext):
        try:
            if message.from_user.id in telegram_bot_settings["user_id"]:
                return await func(message)
            else:
                await message.answer("Вы не имеете доступа к этой команде.")
        except TypeError:
            if message.from_user.id in telegram_bot_settings["user_id"]:
                return await func(message, state)
            else:
                await message.answer("Вы не имеете доступа к этой команде.")

    return wrapped
