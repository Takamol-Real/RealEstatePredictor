from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional

class ProjectType(Enum):
    SHOPPING_MALL = "مول تجاري"
    RESIDENTIAL = "سكني"
    COMMERCIAL = "تجاري"
    MIXED_USE = "متعدد الاستخدامات"
    VILLA = "فلل سكنية"
    SINGLE_VILLA = "فيلا سكنية مفردة"
    RESIDENTIAL_COMPOUND = "مجمع سكني"
    ADMIN_BUILDING = "مبنى إداري"

@dataclass
class BuildingRatios:
    ground_floor: float
    upper_floors: float
    top_floor: float

    @classmethod
    def create(cls, floors: int):
        if floors > 4:
            return cls(ground_floor=0.35, upper_floors=0.45, top_floor=0.70)
        return cls(ground_floor=0.65, upper_floors=0.75, top_floor=0.70)

@dataclass
class BuildingParameters:
    land_area: float
    location: str
    floors: int
    project_type: ProjectType
    effective_land_ratio: Optional[float] = None