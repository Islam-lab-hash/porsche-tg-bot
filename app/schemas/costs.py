from pydantic import BaseModel


class CurrencyRates(BaseModel):
    usd_rub: float = 92.0
    eur_rub: float = 100.0


class ImportCostResult(BaseModel):
    auction_fee_rub: int = 0
    delivery_to_port_rub: int = 0
    export_docs_rub: int = 0
    shipping_to_russia_rub: int = 0
    customs_duty_rub: int = 0
    customs_fee_rub: int = 0
    recycling_fee_rub: int = 0
    broker_fee_rub: int = 0
    sbkts_epts_rub: int = 0
    glonass_rub: int = 0
    delivery_inside_russia_rub: int = 0
    mandatory_import_cost: int = 0
    is_estimated: bool = True
    comment: str = ""


class CostCalculation(BaseModel):
    lot_price_rub: int
    auction_fee_rub: int = 0
    delivery_to_port_rub: int = 0
    export_docs_rub: int = 0
    shipping_to_russia_rub: int = 0
    customs_duty_rub: int = 0
    customs_fee_rub: int = 0
    recycling_fee_rub: int = 0
    broker_fee_rub: int = 0
    sbkts_epts_rub: int = 0
    glonass_rub: int = 0
    delivery_inside_russia_rub: int = 0
    repair_min_rub: int
    repair_max_rub: int
    reserve_min_rub: int
    reserve_max_rub: int
    total_min_rub: int
    total_max_rub: int
    budget_rub: int
    fits_budget: bool
    mandatory_import_cost: int = 0
    comment: str = ""
