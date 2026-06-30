from pydantic import BaseModel, Field


class UserSettings(BaseModel):
    budget_rub: int = 4_000_000
    show_foreign: bool = True
    show_flooded: bool = True
    min_score: int = 40
    models: list[str] = Field(default_factory=lambda: ["Panamera", "911"])
    years: list[int] = Field(default_factory=lambda: [2019])
    sources: list[str] = Field(default_factory=lambda: ["mock_ru", "mock_foreign"])
    monitoring_enabled: bool = False
    monitoring_interval_minutes: int = 60


class ScoreResult(BaseModel):
    score: int
    status: str
    reasons: list[str] = Field(default_factory=list)
