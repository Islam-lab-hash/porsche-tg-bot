import re
from decimal import Decimal

from app.schemas.listing import ListingCreate, RawListing
from app.services.currency import CurrencyService
from app.utils.text import compact_text


class ListingNormalizer:
    def __init__(self, currency_service: CurrencyService | None = None) -> None:
        self.currency_service = currency_service or CurrencyService()

    async def normalize(self, raw: RawListing) -> ListingCreate | None:
        text = f"{raw.title} {raw.description or ''}".lower()
        year = self._extract_year(text)
        model = self._extract_model(text)
        if year != 2019 or model not in {"Panamera", "911"}:
            return None
        if model == "Panamera" and "gts" not in text:
            return None

        price_rub = await self._to_rub(raw.price, raw.currency)
        is_foreign = (raw.country or "").lower() not in {"", "россия", "russia", "ru"}
        return ListingCreate(
            source=raw.source,
            source_listing_id=raw.source_listing_id,
            url=raw.url,
            title=compact_text(raw.title),
            model=model,
            generation=None,
            year=year,
            price=raw.price,
            currency=raw.currency.upper(),
            price_rub=price_rub,
            location=raw.location,
            country=raw.country or ("USA" if is_foreign else "Россия"),
            mileage_km=raw.mileage_km,
            vin=raw.vin,
            engine_volume_cc=raw.engine_volume_cc,
            horsepower=raw.horsepower,
            condition_text=compact_text(raw.condition_text),
            description=compact_text(raw.description),
            seller_name=raw.seller_name,
            seller_type=raw.seller_type,
            photos=raw.photos,
            is_foreign=is_foreign,
        )

    def _extract_year(self, text: str) -> int:
        match = re.search(r"\b(20\d{2})\b", text)
        return int(match.group(1)) if match else 0

    def _extract_model(self, text: str) -> str:
        if "panamera" in text:
            return "Panamera"
        if re.search(r"\b911\b", text):
            return "911"
        return ""

    async def _to_rub(self, price: Decimal | None, currency: str) -> int:
        if not price:
            return 0
        rate = await self.currency_service.get_rate(currency)
        return int(price * rate)
