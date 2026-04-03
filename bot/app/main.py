import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp.client_exceptions import ClientConnectorError

from app.config import settings
from app.handlers.common import router


def build_bot() -> Bot:
    if settings.telegram_proxy:
        session = AiohttpSession(proxy=settings.telegram_proxy)
        return Bot(token=settings.bot_token, session=session)
    return Bot(token=settings.bot_token)


async def run_polling() -> None:
    bot = build_bot()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def main():
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            await run_polling()
        except (TelegramNetworkError, ClientConnectorError) as exc:
            logging.exception(
                "Telegram is unreachable (%s). Retrying in 5 seconds. "
                "Set TELEGRAM_PROXY in .env or check internet/firewall/VPN to api.telegram.org:443",
                exc,
            )
            await asyncio.sleep(5)
        except Exception:
            logging.exception("Bot crashed with unexpected error")
            raise


if __name__ == "__main__":
    asyncio.run(main())
