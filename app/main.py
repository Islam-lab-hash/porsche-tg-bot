import asyncio

from aiogram import Bot, Dispatcher

from app.bot.router import build_router
from app.config.settings import get_settings
from app.utils.logging import setup_logging


async def main() -> None:
    setup_logging()
    settings = get_settings()
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN is empty. Set it in .env.")
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(build_router())
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
