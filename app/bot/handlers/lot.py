from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards import listing_keyboard
from app.bot.messages import render_listing_card
from app.schemas.search import SearchQuery
from app.services.search_pipeline import SearchPipeline


router = Router()


@router.message(Command("lot"))
async def lot_command(message: Message) -> None:
    parts = message.text.split(maxsplit=1) if message.text else []
    if len(parts) != 2:
        await message.answer("Напиши так: /lot https://...")
        return
    cards = await SearchPipeline().search(SearchQuery(), include_rejected=True)
    card = next((item for item in cards if parts[1] in item.listing.url or item.listing.url in parts[1]), cards[0] if cards else None)
    if not card:
        await message.answer("Не удалось разобрать ссылку.")
        return
    await message.answer(render_listing_card(card), reply_markup=listing_keyboard(card.listing.url), disable_web_page_preview=True)
