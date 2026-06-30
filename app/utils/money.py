def format_rub(value: int | None) -> str:
    if value is None:
        return "не указано"
    return f"{value:,.0f}".replace(",", " ") + " ₽"


def format_range(min_value: int, max_value: int) -> str:
    return f"от {format_rub(min_value)} до {format_rub(max_value)}"
