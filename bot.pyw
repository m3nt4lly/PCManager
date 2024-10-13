import asyncio
import io
import os

import pyautogui
import win32con
import win32gui
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from core.main_menu import main_menu_command
from core.modules.record_video import record_screen
from core.keyboards.main import keyboard_main
from core.keyboards.system import keyboard_system
from core.keyboards.discord import keyboard_discord
from core.keyboards.cmd import keyboard_cmd

from config import telegram_bot_settings, discord_settings
from core.modules.restricted import restricted

bot = Bot(telegram_bot_settings["token"])
dp = Dispatcher(bot, storage=MemoryStorage())


class FormStates(StatesGroup):
    waiting_for_response = State()
    waiting_for_response_dop = State()


def show_discord(hwnd, _):
    window_text = win32gui.GetWindowText(hwnd)

    try:
        if window_text.split(" - ")[1] == "Discord":
            win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)
            win32gui.SetForegroundWindow(hwnd)
    except IndexError:
        pass


async def change_discord_status(status: str):
    win32gui.EnumWindows(show_discord, None)
    pyautogui.click(int(discord_settings["profile_icon_pos"].split(" ")[0]), int(discord_settings["profile_icon_pos"].split(" ")[1]))
    await asyncio.sleep(2)
    pyautogui.dragTo(int(discord_settings["status_button"].split(" ")[0]), int(discord_settings["status_button"].split(" ")[1]))
    await asyncio.sleep(2)

    if status == "online":
        pyautogui.click(int(discord_settings["status_online"].split(" ")[0]), int(discord_settings["status_online"].split(" ")[1]))
    elif status == "sleep":
        pyautogui.click(int(discord_settings["status_sleep"].split(" ")[0]), int(discord_settings["status_sleep"].split(" ")[1]))
    elif status == "dnd":
        pyautogui.click(int(discord_settings["status_dnd"].split(" ")[0]), int(discord_settings["status_dnd"].split(" ")[1]))
    elif status == "offline":
        pyautogui.click(int(discord_settings["status_offline"].split(" ")[0]), int(discord_settings["status_offline"].split(" ")[1]))


@dp.message_handler(commands=['start'])
@restricted
async def start_command(message: types.Message):
    await message.answer("К вашим услугам!", reply_markup=keyboard_main())


@dp.message_handler(lambda message: message.text == "✉ Discord")
@restricted
async def discord_page_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Взаимодействие с Discord: ", reply_markup=keyboard_discord())


@dp.message_handler(lambda message: message.text == "🟢 Онлайн")
@restricted
async def discord_online_command(message: types.Message):
    await change_discord_status("online")
    await bot.send_message(chat_id=message.chat.id, text="Статус: 🟢 Онлайн", reply_markup=keyboard_discord())


@dp.message_handler(lambda message: message.text == "🟠 Неактивен")
@restricted
async def discord_sleep_command(message: types.Message):
    await change_discord_status("sleep")
    await bot.send_message(chat_id=message.chat.id, text="Статус: 🟠 Неактивен", reply_markup=keyboard_discord())


@dp.message_handler(lambda message: message.text == "🔴 Не беспокоить")
@restricted
async def discord_dnd_command(message: types.Message):
    await change_discord_status("dnd")
    await bot.send_message(chat_id=message.chat.id, text="Статус: 🔴 Не беспокоить", reply_markup=keyboard_discord())


@dp.message_handler(lambda message: message.text == "⚪ Невидимка")
@restricted
async def discord_offline_command(message: types.Message):
    await change_discord_status("offline")
    await bot.send_message(chat_id=message.chat.id, text="Статус: ⚪ Невидимка", reply_markup=keyboard_discord())


@dp.message_handler(lambda message: message.text == "🖥 Система")
@restricted
async def system_page_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Взаимодействие с системой: ", reply_markup=keyboard_system())


@dp.message_handler(lambda message: message.text == "📸 Скриншот")
@restricted
async def screenshot_command(message: types.Message):
    screenshot = pyautogui.screenshot()
    temp_file = io.BytesIO()
    screenshot.save(temp_file, format="PNG")
    temp_file.seek(0)
    await bot.send_photo(photo=temp_file, chat_id=message.chat.id)


@dp.message_handler(lambda message: message.text == "📹 Запись (10 секунд)")
@restricted
async def video_command(message: types.Message):
    record_screen("output_video.mp4")
    video_path = "core/video_output/output_video.mp4"
    await bot.send_video(chat_id=message.chat.id, video=types.InputFile(video_path))


@dp.message_handler(lambda message: message.text == "❌ Блокировка ПК")
@restricted
async def lock_pc_command(message: types.Message):
    os.system("RunDll32.exe user32.dll,LockWorkStation")
    await bot.send_message(chat_id=message.chat.id, text="Ваш компьютер заблокирован.")


@dp.message_handler(lambda message: message.text == "☄ CMD")
@restricted
async def cmd_page_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Взаимодействие с CMD: ", reply_markup=keyboard_cmd())


@dp.message_handler(lambda message: message.text == "✒ Выполнить команду")
@restricted
async def cmd_command(message: types.Message, state: FSMContext):
    await state.set_state(FormStates.waiting_for_response.state)
    await bot.send_message(chat_id=message.chat.id, text="Напиши команду в чат.")


@dp.message_handler(lambda message: message.text == "✒ Выполнить команду (Консоль открыта)")
@restricted
async def cmd_opened_command(message: types.Message, state: FSMContext):
    await state.set_state(FormStates.waiting_for_response_dop.state)
    await bot.send_message(chat_id=message.chat.id, text="Напиши команду в чат.")


@dp.message_handler(state=FormStates.waiting_for_response)
async def process_response(message: types.Message, state: FSMContext):
    await state.finish()
    response = message.text
    os.system(response)


@dp.message_handler(state=FormStates.waiting_for_response_dop)
async def process_response(message: types.Message, state: FSMContext):
    await state.finish()
    response = message.text
    pyautogui.write(response)
    pyautogui.press('enter')


@dp.message_handler(lambda message: message.text == "✔ Открыть консоль")
@restricted
async def open_cmd_command(message: types.Message):
    os.system("start cmd")
    await bot.send_message(chat_id=message.chat.id, text="Консоль была открыта.")


@dp.message_handler(lambda message: message.text == "❌ Закрыть консоль")
@restricted
async def close_cmd_command(message: types.Message):
    os.system("taskkill /IM cmd.exe /F")
    await bot.send_message(chat_id=message.chat.id, text="Консоль была закрыта.")


dp.register_message_handler(main_menu_command, lambda message: message.text == "⏹ Главное меню")


async def on_startup(_):
    for user in telegram_bot_settings["user_id"]:
        await bot.send_message(chat_id=user, text="Бот был запущен!")


async def on_shutdown(_):
    for user in telegram_bot_settings["user_id"]:
        await bot.send_message(chat_id=user, text="Бот был выключен!")


executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
