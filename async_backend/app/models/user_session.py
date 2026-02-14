from dataclasses import dataclass, field


@dataclass
class UserSession:
    user_id: str
    last_region: str = ""
    last_transition_type: str = ""
    last_alerts_shown: list[str] = field(default_factory=list)
    last_update_timestamp: str = ""
