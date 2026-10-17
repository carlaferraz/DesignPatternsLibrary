from dataclasses import dataclass, field
from datetime import datetime

from minilog.core.level import Level


@dataclass(frozen=True)
class LogEvent:
    message: str
    level: Level
    timestamp: datetime = field(default_factory=datetime.now)
