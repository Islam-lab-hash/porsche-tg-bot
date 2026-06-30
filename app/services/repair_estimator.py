import yaml

from app.config.settings import PROJECT_ROOT
from app.schemas.damage import DamageReport
from app.schemas.listing import ListingCreate


class RepairEstimator:
    def __init__(self) -> None:
        with open(PROJECT_ROOT / "app" / "config" / "repair.yaml", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        self.repair_ranges = {key: tuple(value) for key, value in config["repair_ranges"].items()}
        self.expensive_parts = {key: tuple(value) for key, value in config["expensive_parts"].items()}

    def estimate(self, damage: DamageReport, listing: ListingCreate) -> DamageReport:
        base_key = damage.damage_type if damage.damage_type in self.repair_ranges else damage.damage_severity
        repair_min, repair_max = self.repair_ranges.get(base_key, self.repair_ranges["medium"])

        for part in damage.required_parts:
            if part in self.expensive_parts:
                part_min, part_max = self.expensive_parts[part]
                repair_min += int(part_min * 0.35)
                repair_max += int(part_max * 0.55)

        damage.repair_min_rub = repair_min
        damage.repair_max_rub = repair_max
        return damage
