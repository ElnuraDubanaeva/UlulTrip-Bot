from aiogram import types, Dispatcher
from config import admin, bot


async def start_handler(message: types.Message):
    if message.from_user.id not in admin:
        if message.text == "/start":
            await message.answer(
                f"Здравствуйте {message.from_user.first_name}🤗! Добро пожаловать в наш бот!"
                f"\nЯ бот помошник UlulTrip. Чтобы забронировать тур нажмите /arrange"
            )


def register_message_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
