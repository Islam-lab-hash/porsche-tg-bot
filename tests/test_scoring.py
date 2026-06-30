from app.services.customs import CustomsCalculator
from app.services.damage_estimator import DamageEstimator
from app.services.repair_estimator import RepairEstimator
from app.services.scoring import ScoringService


async def test_scoring_penalizes_foreign_import_rejection(foreign_panamera_listing) -> None:
    damage = await DamageEstimator().estimate(foreign_panamera_listing)
    damage = RepairEstimator().estimate(damage, foreign_panamera_listing)
    cost = CustomsCalculator().calculate_total(foreign_panamera_listing, damage, budget_rub=4_000_000)

    score = ScoringService().calculate_score(foreign_panamera_listing, damage, cost)

    assert score.score < 60
    assert any("зарубежный лот" in reason for reason in score.reasons)


async def test_scoring_rewards_clear_ru_listing(ru_911_listing) -> None:
    damage = await DamageEstimator().estimate(ru_911_listing)
    damage = RepairEstimator().estimate(damage, ru_911_listing)
    cost = CustomsCalculator().calculate_total(ru_911_listing, damage, budget_rub=6_000_000)

    score = ScoringService().calculate_score(ru_911_listing, damage, cost)

    assert 0 <= score.score <= 100
    assert any("есть VIN" in reason for reason in score.reasons)
