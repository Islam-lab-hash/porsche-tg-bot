from app.services.customs import CustomsCalculator
from app.services.damage_estimator import DamageEstimator
from app.services.repair_estimator import RepairEstimator


async def test_cost_calculator_adds_repair_and_reserve(ru_911_listing) -> None:
    damage = await DamageEstimator().estimate(ru_911_listing)
    damage = RepairEstimator().estimate(damage, ru_911_listing)
    result = CustomsCalculator().calculate_total(ru_911_listing, damage, budget_rub=5_000_000)

    assert result.reserve_min_rub == int((ru_911_listing.price_rub + damage.repair_min_rub) * 0.10)
    assert result.total_min_rub == ru_911_listing.price_rub + damage.repair_min_rub + result.reserve_min_rub
