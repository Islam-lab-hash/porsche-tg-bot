from pydantic import BaseModel, Field


class VisionDamageResult(BaseModel):
    detected_parts: list[str] = Field(default_factory=list)
    airbags_deployed: bool | None = None
    flood_risk: bool | None = None
    fire_risk: bool | None = None
    geometry_risk: bool | None = None


class DamageReport(BaseModel):
    damage_type: str = "unknown"
    damage_severity: str = "medium"
    risk_level: str = "medium"
    detected_keywords: list[str] = Field(default_factory=list)
    detected_parts: list[str] = Field(default_factory=list)
    airbags_deployed: bool | None = None
    flood_risk: bool | None = None
    fire_risk: bool | None = None
    geometry_risk: bool | None = None
    repair_min_rub: int = 800_000
    repair_max_rub: int = 1_800_000
    required_parts: list[str] = Field(default_factory=list)
    comment: str = "Оценка по тексту объявления, без осмотра и VIN-отчёта."
