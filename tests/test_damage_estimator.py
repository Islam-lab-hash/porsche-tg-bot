from decimal import Decimal

from app.schemas.listing import ListingCreate
from app.services.damage_estimator import DamageEstimator
from app.services.repair_estimator import RepairEstimator


async def test_flood_sets_very_high_risk() -> None:
    listing = ListingCreate(
        source="test",
        source_listing_id="flood",
        url="https://example.local/flood",
        title="Porsche Panamera GTS 2019 утопленник",
        model="Panamera",
        year=2019,
        price=Decimal("1800000"),
        currency="RUB",
        price_rub=1_800_000,
        condition_text="утопленник",
        description="После воды, залиты блоки.",
        photos=[],
    )

    damage = await DamageEstimator().estimate(listing)

    assert damage.damage_type == "flood"
    assert damage.damage_severity == "heavy"
    assert damage.risk_level == "very_high"
    assert damage.flood_risk is True


async def test_missing_engine_detected() -> None:
    listing = ListingCreate(
        source="test",
        source_listing_id="engine",
        url="https://example.local/engine",
        title="Porsche 911 2019 нет двигателя",
        model="911",
        year=2019,
        price=Decimal("1700000"),
        currency="RUB",
        price_rub=1_700_000,
        description="Без мотора, после ДТП.",
        photos=[],
    )

    damage = await DamageEstimator().estimate(listing)
    damage = RepairEstimator().estimate(damage, listing)

    assert damage.damage_type == "engine_missing"
    assert damage.risk_level == "high"
    assert damage.repair_min_rub >= 2_000_000


async def test_missing_transmission_detected() -> None:
    listing = ListingCreate(
        source="test",
        source_listing_id="pdk",
        url="https://example.local/pdk",
        title="Porsche 911 2019 без коробки",
        model="911",
        year=2019,
        price=Decimal("1900000"),
        currency="RUB",
        price_rub=1_900_000,
        description="Нет коробки PDK.",
        photos=[],
    )

    damage = await DamageEstimator().estimate(listing)

    assert damage.damage_type == "transmission_missing"
    assert "PDK" in damage.required_parts
