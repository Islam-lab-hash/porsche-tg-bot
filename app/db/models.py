from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    budget_rub: Mapped[int] = mapped_column(Integer, default=4_000_000)
    show_foreign: Mapped[bool] = mapped_column(Boolean, default=True)
    show_flooded: Mapped[bool] = mapped_column(Boolean, default=True)
    min_score: Mapped[int] = mapped_column(Integer, default=40)

    settings: Mapped["UserSetting"] = relationship(back_populates="user", uselist=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")
    hidden_listings: Mapped[list["HiddenListing"]] = relationship(back_populates="user")


class UserSetting(Base, TimestampMixin):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    models: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=lambda: ["Panamera", "911"])
    years: Mapped[list[int]] = mapped_column(MutableList.as_mutable(JSONB), default=lambda: [2019])
    sources: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=lambda: ["mock_ru", "mock_foreign"])
    monitoring_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    monitoring_interval_minutes: Mapped[int] = mapped_column(Integer, default=60)

    user: Mapped[User] = relationship(back_populates="settings")


class Listing(Base, TimestampMixin):
    __tablename__ = "listings"
    __table_args__ = (
        UniqueConstraint("source", "source_listing_id", name="uq_listing_source_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), index=True)
    source_listing_id: Mapped[str | None] = mapped_column(String(255), index=True)
    url: Mapped[str] = mapped_column(Text, unique=True)
    title: Mapped[str] = mapped_column(Text)
    brand: Mapped[str] = mapped_column(String(80), default="Porsche")
    model: Mapped[str] = mapped_column(String(80), index=True)
    generation: Mapped[str | None] = mapped_column(String(120))
    year: Mapped[int] = mapped_column(Integer, index=True)
    price: Mapped[float | None] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(10), default="RUB")
    price_rub: Mapped[int] = mapped_column(Integer)
    location: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(120))
    mileage_km: Mapped[int | None] = mapped_column(Integer)
    vin: Mapped[str | None] = mapped_column(String(32), index=True)
    engine_volume_cc: Mapped[int | None] = mapped_column(Integer)
    horsepower: Mapped[int | None] = mapped_column(Integer)
    transmission: Mapped[str | None] = mapped_column(String(80))
    drive_type: Mapped[str | None] = mapped_column(String(80))
    condition_text: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    seller_name: Mapped[str | None] = mapped_column(String(255))
    seller_type: Mapped[str | None] = mapped_column(String(80))
    photos: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=list)
    is_foreign: Mapped[bool] = mapped_column(Boolean, default=False)
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DamageReport(Base):
    __tablename__ = "damage_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), index=True)
    damage_type: Mapped[str] = mapped_column(String(80), default="unknown")
    damage_severity: Mapped[str] = mapped_column(String(80), default="medium")
    risk_level: Mapped[str] = mapped_column(String(80), default="medium")
    detected_keywords: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=list)
    detected_parts: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=list)
    airbags_deployed: Mapped[bool | None] = mapped_column(Boolean)
    flood_risk: Mapped[bool | None] = mapped_column(Boolean)
    fire_risk: Mapped[bool | None] = mapped_column(Boolean)
    geometry_risk: Mapped[bool | None] = mapped_column(Boolean)
    repair_min_rub: Mapped[int] = mapped_column(Integer)
    repair_max_rub: Mapped[int] = mapped_column(Integer)
    required_parts: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSONB), default=list)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CostCalculation(Base):
    __tablename__ = "cost_calculations"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), index=True)
    lot_price_rub: Mapped[int] = mapped_column(Integer)
    auction_fee_rub: Mapped[int] = mapped_column(Integer, default=0)
    delivery_to_port_rub: Mapped[int] = mapped_column(Integer, default=0)
    export_docs_rub: Mapped[int] = mapped_column(Integer, default=0)
    shipping_to_russia_rub: Mapped[int] = mapped_column(Integer, default=0)
    customs_duty_rub: Mapped[int] = mapped_column(Integer, default=0)
    customs_fee_rub: Mapped[int] = mapped_column(Integer, default=0)
    recycling_fee_rub: Mapped[int] = mapped_column(Integer, default=0)
    broker_fee_rub: Mapped[int] = mapped_column(Integer, default=0)
    sbkts_epts_rub: Mapped[int] = mapped_column(Integer, default=0)
    glonass_rub: Mapped[int] = mapped_column(Integer, default=0)
    delivery_inside_russia_rub: Mapped[int] = mapped_column(Integer, default=0)
    repair_min_rub: Mapped[int] = mapped_column(Integer)
    repair_max_rub: Mapped[int] = mapped_column(Integer)
    reserve_min_rub: Mapped[int] = mapped_column(Integer)
    reserve_max_rub: Mapped[int] = mapped_column(Integer)
    total_min_rub: Mapped[int] = mapped_column(Integer)
    total_max_rub: Mapped[int] = mapped_column(Integer)
    budget_rub: Mapped[int] = mapped_column(Integer)
    fits_budget: Mapped[bool] = mapped_column(Boolean)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uq_favorite_user_listing"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="favorites")


class HiddenListing(Base):
    __tablename__ = "hidden_listings"
    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uq_hidden_user_listing"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="hidden_listings")


class SentListing(Base):
    __tablename__ = "sent_listings"
    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uq_sent_user_listing"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    sent_price_rub: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SourceError(Base):
    __tablename__ = "source_errors"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), index=True)
    url: Mapped[str | None] = mapped_column(Text)
    error_type: Mapped[str] = mapped_column(String(120))
    error_message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
