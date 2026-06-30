from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.db.models import Listing, User, UserSetting
from app.schemas.listing import ListingCreate


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str | None = None) -> User:
    settings = get_settings()
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        return user

    user = User(
        telegram_id=telegram_id,
        username=username,
        budget_rub=settings.default_budget_rub,
        show_foreign=True,
        show_flooded=True,
        min_score=40,
    )
    session.add(user)
    await session.flush()
    session.add(
        UserSetting(
            user_id=user.id,
            monitoring_interval_minutes=settings.default_monitoring_interval_minutes,
        )
    )
    await session.commit()
    return user


async def set_user_budget(session: AsyncSession, telegram_id: int, budget_rub: int) -> User:
    user = await get_or_create_user(session, telegram_id)
    user.budget_rub = budget_rub
    await session.commit()
    return user


async def save_listing(session: AsyncSession, listing: ListingCreate) -> Listing:
    existing = await session.execute(select(Listing).where(Listing.url == listing.url))
    db_listing = existing.scalar_one_or_none()
    if db_listing:
        db_listing.last_seen_at = datetime.utcnow()
        if db_listing.price_rub != listing.price_rub:
            db_listing.price_rub = listing.price_rub
            db_listing.price = listing.price
        await session.commit()
        return db_listing

    db_listing = Listing(**listing.model_dump())
    session.add(db_listing)
    await session.commit()
    await session.refresh(db_listing)
    return db_listing
