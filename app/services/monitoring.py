import logging

from aiogram import Bot

from app.schemas.search import SearchQuery
from app.services.notifier import Notifier
from app.services.search_pipeline import SearchPipeline


logger = logging.getLogger(__name__)


class MonitoringService:
    def __init__(self, bot: Bot) -> None:
        self.pipeline = SearchPipeline()
        self.notifier = Notifier(bot)

    async def run_for_user(self, telegram_id: int, query: SearchQuery) -> None:
        cards = await self.pipeline.search(query, include_rejected=False)
        for card in cards:
            await self.notifier.send_listing_card(telegram_id, card)
        logger.info("monitoring sent %s cards to %s", len(cards), telegram_id)
