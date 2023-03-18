from aiogram import types, Dispatcher
from config import admin
from database.bot_db import get_qr_code, get_category, get_guide
from config import bot


async def qr_code_echo(message: types.Message):
    tour = await get_qr_code(message.text)
    category = await get_category(tour[13])
    guide = await get_guide(tour[14])
    site = f"<a href='http://164.92.190.147:8880/home/tour/{tour[4]}'>Tour</a>"
    await message.answer(
        f"\nТур: <i>{tour[1]}</i>"
        f"\nЦена: <i>{tour[3]}</i>"
        f"\nДата выезда: <i>{tour[6]}</i>"
        f"\nДата приезда: <i>{tour[7]}</i>"
        f"\nЛимит: <i>{tour[8]}</i>"
        f"\nСколько: <i>{tour[9]}</i>"
        f"\nДлительность: <i>{tour[11]} дней</i>"
        f"\nСложность: <i>{tour[12]}</i>"
        f"\nГид: <i>{guide[0]} {guide[1]}</i>"
        f"\nКатегория: <i>{category[0]}</i>"
        f"\nSite: <i>{site}</i>",
        parse_mode="HTML",
    )


async def start_handler(message: types.Message):
    if message.from_user.id not in admin:
        if message.text == '/start':
            await message.answer(
                f"Здравствуйте {message.from_user.first_name}🤗!\n Добро пожаловать в наш бот!"
                f" Я бот помошник UlulTrip. Чтобы забронировать тур отправь мне код"
            )
        else:
            data = message.text
            print(data)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='/start')
    else:
        await message.answer(
            "/admin"
        )


def register_message_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(qr_code_echo, )
