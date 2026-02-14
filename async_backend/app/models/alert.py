from dataclasses import dataclass


@dataclass
class Alert:
    id: str
    category: str
    severity: str
    summary: str
    confidence: float
    delivery: str = "dashboard"  # "push" | "dashboard"
