from decimal import Decimal

import yaml

from app.config.settings import PROJECT_ROOT
from app.schemas.costs import CostCalculation, ImportCostResult
from app.schemas.damage import DamageReport
from app.schemas.listing import ListingCreate


class CustomsCalculator:
    def __init__(self) -> None:
        with open(PROJECT_ROOT / "app" / "config" / "customs.yaml", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)["customs"]

    def calculate_import_cost(self, listing: ListingCreate) -> ImportCostResult:
        if not listing.is_foreign:
            return ImportCostResult(comment="Авто находится в РФ, импортные платежи не считаются.")

        engine_cc = listing.engine_volume_cc or (3996 if listing.model == "Panamera" else 2981)
        duty_rate = Decimal(str(self.config["duty_rates"]["passenger_car"]["over_3000_cc"]))
        if 2300 <= engine_cc <= 3000:
            duty_rate = Decimal(str(self.config["duty_rates"]["passenger_car"]["2300_3000_cc"]))

        customs_duty = int(Decimal(engine_cc) * duty_rate * Decimal("100"))
        recycling_fee = self._recycling_fee(listing)
        result = ImportCostResult(
            auction_fee_rub=self.config["auction_fee_default"],
            delivery_to_port_rub=self.config["delivery_to_port_default"],
            export_docs_rub=self.config["export_docs_default"],
            shipping_to_russia_rub=self.config["shipping_to_russia_default"],
            customs_duty_rub=customs_duty,
            customs_fee_rub=self.config["customs_fee_default"],
            recycling_fee_rub=recycling_fee,
            broker_fee_rub=self.config["broker_fee_default"],
            sbkts_epts_rub=self.config["sbkts_epts_default"],
            glonass_rub=self.config["glonass_default"],
            delivery_inside_russia_rub=self.config["delivery_inside_russia_default"],
            is_estimated=True,
            comment=(
                "Ставки утильсбора, пошлины и таможенных платежей могут меняться. "
                "Перед реальным использованием нужно обновлять конфиг по актуальным источникам."
            ),
        )
        result.mandatory_import_cost = (
            result.customs_duty_rub
            + result.customs_fee_rub
            + result.recycling_fee_rub
            + result.broker_fee_rub
            + result.sbkts_epts_rub
            + result.glonass_rub
        )
        return result

    def calculate_total(self, listing: ListingCreate, damage: DamageReport, budget_rub: int) -> CostCalculation:
        imports = self.calculate_import_cost(listing)
        reserve_min = int((listing.price_rub + damage.repair_min_rub) * 0.10)
        reserve_max = int((listing.price_rub + damage.repair_max_rub) * 0.15)
        import_total = (
            imports.auction_fee_rub
            + imports.delivery_to_port_rub
            + imports.export_docs_rub
            + imports.shipping_to_russia_rub
            + imports.customs_duty_rub
            + imports.customs_fee_rub
            + imports.recycling_fee_rub
            + imports.broker_fee_rub
            + imports.sbkts_epts_rub
            + imports.glonass_rub
            + imports.delivery_inside_russia_rub
        )
        total_min = listing.price_rub + import_total + damage.repair_min_rub + reserve_min
        total_max = listing.price_rub + import_total + damage.repair_max_rub + reserve_max

        fits_budget = total_min <= budget_rub
        comment = "Проходит по нижней границе бюджета." if fits_budget else f"Не проходит бюджет {budget_rub} ₽."
        if listing.is_foreign and imports.mandatory_import_cost > budget_rub:
            fits_budget = False
            comment = "❌ Не проходит: обязательные платежи при ввозе выше бюджета"

        return CostCalculation(
            lot_price_rub=listing.price_rub,
            auction_fee_rub=imports.auction_fee_rub,
            delivery_to_port_rub=imports.delivery_to_port_rub,
            export_docs_rub=imports.export_docs_rub,
            shipping_to_russia_rub=imports.shipping_to_russia_rub,
            customs_duty_rub=imports.customs_duty_rub,
            customs_fee_rub=imports.customs_fee_rub,
            recycling_fee_rub=imports.recycling_fee_rub,
            broker_fee_rub=imports.broker_fee_rub,
            sbkts_epts_rub=imports.sbkts_epts_rub,
            glonass_rub=imports.glonass_rub,
            delivery_inside_russia_rub=imports.delivery_inside_russia_rub,
            repair_min_rub=damage.repair_min_rub,
            repair_max_rub=damage.repair_max_rub,
            reserve_min_rub=reserve_min,
            reserve_max_rub=reserve_max,
            total_min_rub=total_min,
            total_max_rub=total_max,
            budget_rub=budget_rub,
            fits_budget=fits_budget,
            mandatory_import_cost=imports.mandatory_import_cost,
            comment=comment,
        )

    def _recycling_fee(self, listing: ListingCreate) -> int:
        recycling = self.config["recycling_fee"]
        if listing.model == "Panamera":
            return recycling["panamera_gts_2019_default"]
        return recycling["porsche_911_2019_default_max"]
