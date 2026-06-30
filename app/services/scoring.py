from app.schemas.costs import CostCalculation
from app.schemas.damage import DamageReport
from app.schemas.listing import ListingCreate
from app.schemas.user import ScoreResult


class ScoringService:
    def calculate_score(self, listing: ListingCreate, damage: DamageReport, cost: CostCalculation) -> ScoreResult:
        score = 50
        reasons: list[str] = []

        if cost.fits_budget:
            score += 15
            reasons.append("+15 цена укладывается в бюджет по нижней границе")
        if listing.vin:
            score += 10
            reasons.append("+10 есть VIN")
        else:
            score -= 20
            reasons.append("-20 нет VIN")
        if len(listing.photos) >= 5:
            score += 10
            reasons.append("+10 много фото")
        else:
            score -= 15
            reasons.append("-15 мало фото")
        if not listing.is_foreign:
            score += 10
            reasons.append("+10 авто в РФ")
        if damage.damage_type != "unknown":
            score += 10
            reasons.append("+10 понятные повреждения")
        if damage.flood_risk:
            score -= 25
            reasons.append("-25 утопленник")
        if damage.fire_risk:
            score -= 25
            reasons.append("-25 пожар")
        if damage.damage_type == "engine_missing":
            score -= 20
            reasons.append("-20 нет двигателя")
        if damage.damage_type == "transmission_missing":
            score -= 15
            reasons.append("-15 нет коробки")
        if damage.geometry_risk:
            score -= 25
            reasons.append("-25 риск геометрии")
        if damage.airbags_deployed:
            score -= 20
            reasons.append("-20 сработали подушки")
        if listing.is_foreign and cost.mandatory_import_cost > cost.budget_rub:
            score -= 30
            reasons.append("-30 зарубежный лот не проходит по ввозу")

        score = max(0, min(100, score))
        return ScoreResult(score=score, status=self._status(score), reasons=reasons)

    def _status(self, score: int) -> str:
        if score >= 80:
            return "хороший вариант для проверки"
        if score >= 60:
            return "можно смотреть"
        if score >= 40:
            return "рискованно"
        return "лучше пропустить"
