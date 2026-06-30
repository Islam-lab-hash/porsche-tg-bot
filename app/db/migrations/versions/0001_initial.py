"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-30
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("budget_rub", sa.Integer(), nullable=False),
        sa.Column("show_foreign", sa.Boolean(), nullable=False),
        sa.Column("show_flooded", sa.Boolean(), nullable=False),
        sa.Column("min_score", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=True)

    op.create_table(
        "user_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("models", postgresql.JSONB(), nullable=False),
        sa.Column("years", postgresql.JSONB(), nullable=False),
        sa.Column("sources", postgresql.JSONB(), nullable=False),
        sa.Column("monitoring_enabled", sa.Boolean(), nullable=False),
        sa.Column("monitoring_interval_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("source_listing_id", sa.String(length=255), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("brand", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=80), nullable=False),
        sa.Column("generation", sa.String(length=120), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(14, 2), nullable=True),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("price_rub", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("mileage_km", sa.Integer(), nullable=True),
        sa.Column("vin", sa.String(length=32), nullable=True),
        sa.Column("engine_volume_cc", sa.Integer(), nullable=True),
        sa.Column("horsepower", sa.Integer(), nullable=True),
        sa.Column("transmission", sa.String(length=80), nullable=True),
        sa.Column("drive_type", sa.String(length=80), nullable=True),
        sa.Column("condition_text", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("seller_name", sa.String(length=255), nullable=True),
        sa.Column("seller_type", sa.String(length=80), nullable=True),
        sa.Column("photos", postgresql.JSONB(), nullable=False),
        sa.Column("is_foreign", sa.Boolean(), nullable=False),
        sa.Column("is_new", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("first_seen_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("source", "source_listing_id", name="uq_listing_source_id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index("ix_listings_model", "listings", ["model"])
    op.create_index("ix_listings_source", "listings", ["source"])
    op.create_index("ix_listings_source_listing_id", "listings", ["source_listing_id"])
    op.create_index("ix_listings_vin", "listings", ["vin"])
    op.create_index("ix_listings_year", "listings", ["year"])

    op.create_table(
        "damage_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("damage_type", sa.String(length=80), nullable=False),
        sa.Column("damage_severity", sa.String(length=80), nullable=False),
        sa.Column("risk_level", sa.String(length=80), nullable=False),
        sa.Column("detected_keywords", postgresql.JSONB(), nullable=False),
        sa.Column("detected_parts", postgresql.JSONB(), nullable=False),
        sa.Column("airbags_deployed", sa.Boolean(), nullable=True),
        sa.Column("flood_risk", sa.Boolean(), nullable=True),
        sa.Column("fire_risk", sa.Boolean(), nullable=True),
        sa.Column("geometry_risk", sa.Boolean(), nullable=True),
        sa.Column("repair_min_rub", sa.Integer(), nullable=False),
        sa.Column("repair_max_rub", sa.Integer(), nullable=False),
        sa.Column("required_parts", postgresql.JSONB(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_damage_reports_listing_id", "damage_reports", ["listing_id"])

    op.create_table(
        "cost_calculations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("lot_price_rub", sa.Integer(), nullable=False),
        sa.Column("auction_fee_rub", sa.Integer(), nullable=False),
        sa.Column("delivery_to_port_rub", sa.Integer(), nullable=False),
        sa.Column("export_docs_rub", sa.Integer(), nullable=False),
        sa.Column("shipping_to_russia_rub", sa.Integer(), nullable=False),
        sa.Column("customs_duty_rub", sa.Integer(), nullable=False),
        sa.Column("customs_fee_rub", sa.Integer(), nullable=False),
        sa.Column("recycling_fee_rub", sa.Integer(), nullable=False),
        sa.Column("broker_fee_rub", sa.Integer(), nullable=False),
        sa.Column("sbkts_epts_rub", sa.Integer(), nullable=False),
        sa.Column("glonass_rub", sa.Integer(), nullable=False),
        sa.Column("delivery_inside_russia_rub", sa.Integer(), nullable=False),
        sa.Column("repair_min_rub", sa.Integer(), nullable=False),
        sa.Column("repair_max_rub", sa.Integer(), nullable=False),
        sa.Column("reserve_min_rub", sa.Integer(), nullable=False),
        sa.Column("reserve_max_rub", sa.Integer(), nullable=False),
        sa.Column("total_min_rub", sa.Integer(), nullable=False),
        sa.Column("total_max_rub", sa.Integer(), nullable=False),
        sa.Column("budget_rub", sa.Integer(), nullable=False),
        sa.Column("fits_budget", sa.Boolean(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_cost_calculations_listing_id", "cost_calculations", ["listing_id"])

    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "listing_id", name="uq_favorite_user_listing"),
    )
    op.create_table(
        "hidden_listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "listing_id", name="uq_hidden_user_listing"),
    )
    op.create_table(
        "sent_listings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("listings.id"), nullable=False),
        sa.Column("sent_price_rub", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "listing_id", name="uq_sent_user_listing"),
    )

    op.create_table(
        "source_errors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("error_type", sa.String(length=120), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_source_errors_source", "source_errors", ["source"])


def downgrade() -> None:
    op.drop_table("source_errors")
    op.drop_table("sent_listings")
    op.drop_table("hidden_listings")
    op.drop_table("favorites")
    op.drop_table("cost_calculations")
    op.drop_table("damage_reports")
    op.drop_table("listings")
    op.drop_table("user_settings")
    op.drop_table("users")
