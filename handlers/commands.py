from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_not_admins_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand("/start", "Чтобы начать или же перезапустить бот"),
            BotCommand("/info", "Чтобы получить информацию"),
            BotCommand("/arrange", "Чтобы забронировать тур"),
        ],
        scope=BotCommandScopeChat(chat_id),
    )