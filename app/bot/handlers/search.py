from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards import listing_keyboard
from app.bot.messages import render_listing_card
from app.config.settings import get_settings
from app.db.repositories import get_or_create_user, save_listing
from app.db.session import SessionLocal
from app.schemas.search import SearchQuery
from app.services.search_pipeline import SearchPipeline


router = Router()


@router.message(Command("search"))
@router.message(F.text == "🔍 Начать поиск")
async def search_command(message: Message) -> None:
    await message.answer("Ищу Porsche по текущим настройкам...")
    settings = get_settings()
    budget = settings.default_budget_rub
    try:
        async with SessionLocal() as session:
            user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
            budget = user.budget_rub
    except Exception:
        pass

    query = SearchQuery(budget_rub=budget)
    cards = await SearchPipeline().search(query, include_rejected=settings.show_rejected_in_manual_search)
    if not cards:
        await message.answer("Пока ничего не нашёл.")
        return

    for card in cards:
        try:
            async with SessionLocal() as session:
                await save_listing(session, card.listing)
        except Exception:
            pass
        await message.answer(
            render_listing_card(card),
            reply_markup=listing_keyboard(card.listing.url),
            disable_web_page_preview=True,
        )
