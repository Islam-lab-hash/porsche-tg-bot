from app.parsers.base import safe_search
from app.parsers.mock import MockForeignParser, MockRuParser
from app.schemas.listing import ListingCard
from app.schemas.search import SearchQuery
from app.services.customs import CustomsCalculator
from app.services.damage_estimator import DamageEstimator
from app.services.listing_normalizer import ListingNormalizer
from app.services.repair_estimator import RepairEstimator
from app.services.scoring import ScoringService


class SearchPipeline:
    def __init__(self) -> None:
        self.parsers = {
            "mock_ru": MockRuParser(),
            "mock_foreign": MockForeignParser(),
        }
        self.normalizer = ListingNormalizer()
        self.damage_estimator = DamageEstimator()
        self.repair_estimator = RepairEstimator()
        self.customs = CustomsCalculator()
        self.scoring = ScoringService()

    async def search(self, query: SearchQuery, include_rejected: bool = True) -> list[ListingCard]:
        cards: list[ListingCard] = []
        for source in query.sources:
            parser = self.parsers.get(source)
            if not parser:
                continue
            raw_listings = await safe_search(parser, query)
            for raw in raw_listings:
                listing = await self.normalizer.normalize(raw)
                if not listing:
                    continue
                if listing.is_foreign and not query.show_foreign:
                    continue
                damage = await self.damage_estimator.estimate(listing)
                damage = self.repair_estimator.estimate(damage, listing)
                if damage.flood_risk and not query.show_flooded:
                    continue
                cost = self.customs.calculate_total(listing, damage, query.budget_rub)
                score = self.scoring.calculate_score(listing, damage, cost)
                if include_rejected or (cost.fits_budget and score.score >= query.min_score):
                    cards.append(ListingCard(listing=listing, damage=damage, cost=cost, score=score))
        return cards
