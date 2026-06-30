from decimal import Decimal

import pytest

from app.schemas.listing import ListingCreate


@pytest.fixture
def ru_911_listing() -> ListingCreate:
    return ListingCreate(
        source="test",
        source_listing_id="1",
        url="https://example.local/911",
        title="Porsche 911 Carrera S 2019 после ДТП",
        model="911",
        year=2019,
        price=Decimal("2400000"),
        currency="RUB",
        price_rub=2_400_000,
        country="Россия",
        location="Москва",
        mileage_km=82_000,
        vin="WP0ZZZ99ZKS123456",
        engine_volume_cc=2981,
        horsepower=450,
        condition_text="после ДТП, не на ходу",
        description="Удар спереди, сработали подушки, нужны фары и радиаторы.",
        photos=["1", "2", "3", "4", "5"],
        is_foreign=False,
    )


@pytest.fixture
def foreign_panamera_listing() -> ListingCreate:
    return ListingCreate(
        source="test",
        source_listing_id="2",
        url="https://example.local/panamera",
        title="2019 Porsche Panamera GTS salvage",
        model="Panamera",
        year=2019,
        price=Decimal("9000"),
        currency="USD",
        price_rub=828_000,
        country="USA",
        location="New Jersey",
        mileage_km=61_000,
        vin="WP0AF2A75KL123456",
        engine_volume_cc=3996,
        horsepower=453,
        condition_text="salvage",
        description="Front damage, airbags deployed.",
        photos=["1", "2", "3"],
        is_foreign=True,
    )
