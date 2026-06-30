from datetime import date
from decimal import Decimal

import httpx


class CurrencyService:
    def __init__(self) -> None:
        self._cache: dict[tuple[str, date], Decimal] = {}
        self._fallback = {"USD": Decimal("92.0"), "EUR": Decimal("100.0"), "RUB": Decimal("1.0")}

    async def get_rate(self, currency: str) -> Decimal:
        currency = currency.upper()
        if currency == "RUB":
            return Decimal("1.0")
        today_key = (currency, date.today())
        if today_key in self._cache:
            return self._cache[today_key]

        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
                response.raise_for_status()
                data = response.json()
                rate = Decimal(str(data["Valute"][currency]["Value"]))
        except Exception:
            rate = self._fallback.get(currency, Decimal("1.0"))

        self._cache[today_key] = rate
        self._fallback[currency] = rate
        return rate
