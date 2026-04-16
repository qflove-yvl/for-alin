import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiohttp.client_exceptions import ClientConnectorError

from app.config import settings
from app.handlers.common import router


def build_bot() -> Bot:
    if settings.telegram_proxy:
        session = AiohttpSession(proxy=settings.telegram_proxy)
        return Bot(token=settings.bot_token, session=session)
    return Bot(token=settings.bot_token)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск и меню"),
            BotCommand(command="help", description="Список команд"),
            BotCommand(command="cancel", description="Отменить текущий сценарий"),
            BotCommand(command="create_poll", description="Создать опрос"),
            BotCommand(command="my_polls", description="Мои опросы"),
            BotCommand(command="take_poll", description="Пройти опрос"),
            BotCommand(command="results", description="Результаты /results <id>"),
        ]
    )


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = build_bot()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    try:
        while True:
            try:
                await set_commands(bot)
                await dp.start_polling(bot)
            except (TelegramNetworkError, ClientConnectorError) as exc:
                logging.warning(
                    "Telegram unreachable: %s. Retrying in 5s. "
                    "Set TELEGRAM_PROXY in .env or check firewall/VPN.",
                    exc,
                )
                await asyncio.sleep(5)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
