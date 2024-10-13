from aiogram import types
from aiogram.dispatcher import FSMContext
from core.modules.restricted import restricted
from core.keyboards.main import keyboard_main


@restricted
async def main_menu_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("К вашим услугам!", reply_markup=keyboard_main())
