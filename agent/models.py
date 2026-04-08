from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional


ActionType = Literal["ask", "confirm", "accept", "postpone"]


@dataclass
class FieldValue:
    value: Any
    source: str
    confidence: float
    status: Literal["missing", "inferred", "confirmed", "user_provided"]


@dataclass
class UserBehavior:
    patience_level: int = 10
    time_on_page_sec: int = 0
    hesitation_events: int = 0
    device_type: Optional[str] = None


@dataclass
class UserState:
    fields: Dict[str, FieldValue] = field(default_factory=dict)
    question_history: List[str] = field(default_factory=list)
    behavior: UserBehavior = field(default_factory=UserBehavior)


@dataclass
class Decision:
    field_name: str
    action: ActionType
    reason: str
    question_text: Optional[str] = None
    options: Optional[List[str]] = None