from app.services.customs import CustomsCalculator
from app.services.damage_estimator import DamageEstimator
from app.services.repair_estimator import RepairEstimator


async def test_foreign_panamera_rejected_if_import_cost_higher_than_budget(foreign_panamera_listing) -> None:
    damage = await DamageEstimator().estimate(foreign_panamera_listing)
    damage = RepairEstimator().estimate(damage, foreign_panamera_listing)
    result = CustomsCalculator().calculate_total(foreign_panamera_listing, damage, budget_rub=4_000_000)

    assert result.fits_budget is False
    assert result.mandatory_import_cost > 4_000_000
    assert "обязательные платежи" in result.comment


async def test_ru_listing_budget_filter(ru_911_listing) -> None:
    damage = await DamageEstimator().estimate(ru_911_listing)
    damage = RepairEstimator().estimate(damage, ru_911_listing)
    result = CustomsCalculator().calculate_total(ru_911_listing, damage, budget_rub=3_000_000)

    assert result.total_min_rub > 0
    assert result.budget_rub == 3_000_000
    assert result.fits_budget is False
