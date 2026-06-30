import re


def compact_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def contains_any(text: str, needles: list[str]) -> list[str]:
    normalized = text.lower()
    return [needle for needle in needles if needle.lower() in normalized]
