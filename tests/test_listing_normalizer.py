from app.parsers.mock import MockForeignParser, MockRuParser
from app.schemas.search import SearchQuery
from app.services.listing_normalizer import ListingNormalizer


async def test_detects_panamera_gts() -> None:
    raw = (await MockForeignParser().search(SearchQuery()))[0]
    listing = await ListingNormalizer().normalize(raw)

    assert listing is not None
    assert listing.model == "Panamera"
    assert listing.year == 2019
    assert listing.is_foreign is True


async def test_detects_porsche_911() -> None:
    raw = (await MockRuParser().search(SearchQuery()))[0]
    listing = await ListingNormalizer().normalize(raw)

    assert listing is not None
    assert listing.model == "911"
    assert listing.year == 2019
    assert listing.is_foreign is False
