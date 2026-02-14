from dataclasses import dataclass, field


@dataclass
class Region:
    id: str
    type: str  # "state" | "city" | "zone"
    parent_region: str | None = None
    dominant_language: str = ""
    cultural_markers: list[str] = field(default_factory=list)
    legal_rules: list[str] = field(default_factory=list)
    behavioral_notes: list[str] = field(default_factory=list)
