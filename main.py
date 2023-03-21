from aiogram import Bot
from aiogram.utils import executor
import logging
from config import dp, bot
from database.bot_db import connect_postgresql
from handlers import client, fsm_user




async def on_startup(_):
    connect_postgresql()


client.register_message_handler_client(dp)
fsm_user.register_handlers_fsm_student(dp)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
