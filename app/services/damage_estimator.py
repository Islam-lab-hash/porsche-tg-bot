import yaml

from app.config.settings import PROJECT_ROOT
from app.schemas.damage import DamageReport, VisionDamageResult
from app.schemas.listing import ListingCreate
from app.utils.text import contains_any


class VisionDamageAnalyzer:
    async def analyze_photos(self, photo_urls: list[str]) -> VisionDamageResult:
        return VisionDamageResult()


class DamageEstimator:
    def __init__(self, vision: VisionDamageAnalyzer | None = None) -> None:
        self.vision = vision or VisionDamageAnalyzer()
        with open(PROJECT_ROOT / "app" / "config" / "keywords.yaml", encoding="utf-8") as file:
            self.keywords = yaml.safe_load(file)["damage_keywords"]

    async def estimate(self, listing: ListingCreate) -> DamageReport:
        text = f"{listing.title} {listing.condition_text or ''} {listing.description or ''}".lower()
        detected = contains_any(text, self.keywords)
        vision = await self.vision.analyze_photos(listing.photos)

        damage_type = "unknown"
        severity = "medium"
        risk = "medium"
        parts: list[str] = []
        flood_risk = False
        fire_risk = False
        geometry_risk = False
        airbags = vision.airbags_deployed

        if any(word in text for word in ["утопленник", "утопленная", "flood", "water damage", "залит"]):
            damage_type = "flood"
            severity = "heavy"
            risk = "very_high"
            flood_risk = True
        elif any(word in text for word in ["пожар", "сгорел", "fire"]):
            damage_type = "fire"
            severity = "heavy"
            risk = "very_high"
            fire_risk = True
        elif any(word in text for word in ["нет двигателя", "без двигателя", "нет мотора", "без мотора"]):
            damage_type = "engine_missing"
            severity = "heavy"
            risk = "high"
            parts.append("engine")
        elif any(word in text for word in ["нет коробки", "без коробки"]):
            damage_type = "transmission_missing"
            severity = "heavy"
            risk = "high"
            parts.append("PDK")
        elif any(word in text for word in ["удар спереди", "front", "перед"]):
            damage_type = "front_damage"
            severity = "medium"
            parts.extend(["headlights", "front_radiators"])

        if any(word in text for word in ["геометр", "лонжерон", "стойка"]):
            geometry_risk = True
            risk = "high"
        if any(word in text for word in ["airbag", "подушки", "сработали подушки"]):
            airbags = True
            parts.append("airbags")

        return DamageReport(
            damage_type=damage_type,
            damage_severity=severity,
            risk_level=risk,
            detected_keywords=detected,
            detected_parts=parts + vision.detected_parts,
            airbags_deployed=airbags,
            flood_risk=flood_risk or vision.flood_risk,
            fire_risk=fire_risk or vision.fire_risk,
            geometry_risk=geometry_risk or vision.geometry_risk,
            required_parts=sorted(set(parts + vision.detected_parts)),
        )
