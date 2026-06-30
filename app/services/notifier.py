from aiogram import Bot

from app.bot.messages import render_listing_card
from app.schemas.listing import ListingCard


class Notifier:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_listing_card(self, telegram_id: int, card: ListingCard) -> None:
        await self.bot.send_message(telegram_id, render_listing_card(card), disable_web_page_preview=True)
