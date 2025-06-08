"""
Запуск бота: `python3 -m app.main`
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Update
from aiogram.exceptions import TelegramAPIError
from app.config import get_settings
from app.handlers import common, auth, rates, finance
from app.utils.messages import ERROR_MESSAGE

def setup_logging() -> None:
    """Настраивает формат и уровень логирования для приложения."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
    )

class ErrorHandlerMiddleware:
    """Глобальный обработчик ошибок для aiogram."""
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramAPIError as e:
            logging.exception("Telegram API error: %s", e)
            if hasattr(event, 'message'):
                await event.message.reply(ERROR_MESSAGE)
        except Exception as e:
            logging.exception("Unhandled error: %s", e)
            if hasattr(event, 'message'):
                await event.message.reply(ERROR_MESSAGE)

async def main() -> None:
    setup_logging()
    settings = get_settings()
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()
    dp.message.middleware(ErrorHandlerMiddleware())
    dp.include_routers(
        common.router,
        auth.router,
        rates.router,
        finance.router,
    )
    await dp.start_polling(bot)

if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
