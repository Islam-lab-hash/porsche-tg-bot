from app.schemas.listing import ListingCard
from app.utils.money import format_range, format_rub


START_TEXT = (
    "Бот ищет проблемные Porsche Panamera GTS 2019 и Porsche 911, "
    "считает примерную полную стоимость, ремонт и риск."
)

HELP_TEXT = """Команды:
/start - запуск
/settings - текущие настройки
/search - ручной поиск
/watch - включить мониторинг
/stop - отключить мониторинг
/budget 4000000 - задать бюджет
/sources - источники
/lot https://... - оценить конкретную ссылку
/favorites - избранное
"""


def render_listing_card(card: ListingCard) -> str:
    listing = card.listing
    damage = card.damage
    cost = card.cost
    score = card.score

    vin_status = "есть" if listing.vin else "нет"
    damage_lines = "\n".join([f"- {item}" for item in _damage_lines(card)])
    status_icon = "✅" if cost.fits_budget else "❌"
    status = f"{status_icon} {cost.comment}"

    return f"""{listing.title}

Цена: {format_rub(listing.price_rub)}
Источник: {listing.source}
Город: {listing.location or "не указан"}
Пробег: {format_rub(listing.mileage_km).replace(" ₽", " км") if listing.mileage_km else "не указан"}
VIN: {vin_status}
Состояние: {listing.condition_text or "не указано"}

Повреждения:
{damage_lines}

Оценка ремонта:
{format_range(damage.repair_min_rub, damage.repair_max_rub)}

Итог:
{format_range(cost.total_min_rub, cost.total_max_rub)}

Статус:
{status}

Score: {score.score}/100 ({score.status})
"""


def render_cost_details(card: ListingCard) -> str:
    cost = card.cost
    return f"""Подробный расчёт:
Цена лота: {format_rub(cost.lot_price_rub)}
Комиссии аукциона: {format_rub(cost.auction_fee_rub)}
Доставка и экспорт: {format_rub(cost.delivery_to_port_rub + cost.export_docs_rub + cost.shipping_to_russia_rub)}
Таможня и сборы: {format_rub(cost.customs_duty_rub + cost.customs_fee_rub + cost.recycling_fee_rub)}
Брокер / СБКТС / ЭПТС / ГЛОНАСС: {format_rub(cost.broker_fee_rub + cost.sbkts_epts_rub + cost.glonass_rub)}
Ремонт: {format_range(cost.repair_min_rub, cost.repair_max_rub)}
Резерв: {format_range(cost.reserve_min_rub, cost.reserve_max_rub)}
Итого: {format_range(cost.total_min_rub, cost.total_max_rub)}
"""


def _damage_lines(card: ListingCard) -> list[str]:
    damage = card.damage
    lines = []
    if damage.detected_keywords:
        lines.append("найдены признаки: " + ", ".join(damage.detected_keywords[:6]))
    if damage.required_parts:
        lines.append("возможны узлы: " + ", ".join(damage.required_parts))
    lines.append(f"тип: {damage.damage_type}")
    lines.append(f"риск: {damage.risk_level}")
    if not damage.detected_keywords:
        lines.append("проблемное состояние не подтверждено по ключевым словам")
    return lines
