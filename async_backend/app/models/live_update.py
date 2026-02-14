from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LiveUpdate:
    id: str
    region_id: str
    category: str
    severity: str
    summary: str
    source_links: list[str] = field(default_factory=list)
    source_type: str = ""
    confidence_score: float = 0.5
    effective_from: datetime | None = None
    expires_at: datetime | None = None
    last_updated: datetime | None = None
