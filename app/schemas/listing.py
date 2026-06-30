from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl


class RawListing(BaseModel):
    source: str
    source_listing_id: str | None = None
    url: str
    title: str
    price: Decimal | None = None
    currency: str = "RUB"
    location: str | None = None
    country: str | None = None
    mileage_km: int | None = None
    vin: str | None = None
    engine_volume_cc: int | None = None
    horsepower: int | None = None
    condition_text: str | None = None
    description: str | None = None
    photos: list[str] = Field(default_factory=list)
    seller_name: str | None = None
    seller_type: str | None = None


class ListingCreate(BaseModel):
    source: str
    source_listing_id: str | None
    url: str
    title: str
    brand: str = "Porsche"
    model: str
    generation: str | None = None
    year: int
    price: Decimal | None
    currency: str
    price_rub: int
    location: str | None = None
    country: str = "Россия"
    mileage_km: int | None = None
    vin: str | None = None
    engine_volume_cc: int | None = None
    horsepower: int | None = None
    transmission: str | None = None
    drive_type: str | None = None
    condition_text: str | None = None
    description: str | None = None
    seller_name: str | None = None
    seller_type: str | None = None
    photos: list[str] = Field(default_factory=list)
    is_foreign: bool = False
    is_new: bool = True


class ListingCard(BaseModel):
    listing: ListingCreate
    damage: "DamageReport"
    cost: "CostCalculation"
    score: "ScoreResult"
    created_at: datetime = Field(default_factory=datetime.utcnow)


from app.schemas.costs import CostCalculation  # noqa: E402
from app.schemas.damage import DamageReport  # noqa: E402
from app.schemas.user import ScoreResult  # noqa: E402

ListingCard.model_rebuild()
