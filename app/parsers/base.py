from __future__ import annotations

import asyncio
import logging
from typing import Protocol

from app.schemas.listing import RawListing
from app.schemas.search import SearchQuery


logger = logging.getLogger(__name__)


class BaseSourceParser(Protocol):
    source_name: str

    async def search(self, query: SearchQuery) -> list[RawListing]:
        ...

    async def parse_listing(self, url: str) -> RawListing:
        ...


class RateLimitedParser:
    source_name = "base"
    user_agent = "PorscheBotMVP/0.1 contact: telegram"
    request_timeout_seconds = 15
    max_retries = 3
    rate_limit_seconds = 1.5

    async def _polite_wait(self) -> None:
        await asyncio.sleep(self.rate_limit_seconds)


async def safe_search(parser: BaseSourceParser, query: SearchQuery) -> list[RawListing]:
    try:
        return await parser.search(query)
    except Exception as exc:
        logger.exception("source=%s error=%s", parser.source_name, exc)
        return []
