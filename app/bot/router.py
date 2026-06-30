from aiogram import Router

from app.bot.handlers import favorites, lot, search, settings, start, watch


def build_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(settings.router)
    router.include_router(search.router)
    router.include_router(watch.router)
    router.include_router(lot.router)
    router.include_router(favorites.router)
    return router
