from decimal import Decimal

from app.parsers.base import RateLimitedParser
from app.schemas.listing import RawListing
from app.schemas.search import SearchQuery


class MockRuParser(RateLimitedParser):
    source_name = "mock_ru"

    async def search(self, query: SearchQuery) -> list[RawListing]:
        await self._polite_wait()
        return [
            RawListing(
                source=self.source_name,
                source_listing_id="ru-911-2019-front",
                url="https://example.local/ru/porsche-911-2019-front",
                title="Porsche 911 Carrera S 2019 после ДТП",
                price=Decimal("2450000"),
                currency="RUB",
                location="Москва",
                country="Россия",
                mileage_km=82_000,
                vin="WP0ZZZ99ZKS123456",
                engine_volume_cc=2981,
                horsepower=450,
                condition_text="после ДТП, не на ходу",
                description="Удар спереди, сработали подушки. Нужны фары, радиаторы, капот, телевизор.",
                photos=[
                    "https://example.local/photos/911-1.jpg",
                    "https://example.local/photos/911-2.jpg",
                    "https://example.local/photos/911-3.jpg",
                    "https://example.local/photos/911-4.jpg",
                    "https://example.local/photos/911-5.jpg",
                    "https://example.local/photos/911-6.jpg",
                ],
                seller_name="Страховая реализация",
                seller_type="company",
            ),
            RawListing(
                source=self.source_name,
                source_listing_id="ru-panamera-2019-flood",
                url="https://example.local/ru/porsche-panamera-gts-2019-flood",
                title="Porsche Panamera GTS 2019 утопленник",
                price=Decimal("1850000"),
                currency="RUB",
                location="Санкт-Петербург",
                country="Россия",
                mileage_km=54_000,
                vin=None,
                engine_volume_cc=3996,
                horsepower=460,
                condition_text="утопленник, не заводится",
                description="Автомобиль после воды, залиты блоки управления, требуется ремонт электрики.",
                photos=["https://example.local/photos/panamera-1.jpg"],
                seller_type="private",
            ),
        ]

    async def parse_listing(self, url: str) -> RawListing:
        return (await self.search(SearchQuery()))[0]


class MockForeignParser(RateLimitedParser):
    source_name = "mock_foreign"

    async def search(self, query: SearchQuery) -> list[RawListing]:
        await self._polite_wait()
        return [
            RawListing(
                source=self.source_name,
                source_listing_id="copart-panamera-2019-salvage",
                url="https://example.local/copart/panamera-gts-2019",
                title="2019 Porsche Panamera GTS salvage",
                price=Decimal("9200"),
                currency="USD",
                location="New Jersey",
                country="USA",
                mileage_km=61_000,
                vin="WP0AF2A75KL123456",
                engine_volume_cc=3996,
                horsepower=453,
                condition_text="salvage, front damage",
                description="Run and drive, front end damage, airbags deployed.",
                photos=[
                    "https://example.local/photos/copart-1.jpg",
                    "https://example.local/photos/copart-2.jpg",
                    "https://example.local/photos/copart-3.jpg",
                ],
                seller_type="auction",
            )
        ]

    async def parse_listing(self, url: str) -> RawListing:
        return (await self.search(SearchQuery()))[0]
