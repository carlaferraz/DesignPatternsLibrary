from dataclasses import dataclass, field
from datetime import datetime

from minilog.core.level import Level


@dataclass(frozen=True)
class LogEvent:
    """Um registro de log: o que aconteceu, quão grave e quando.

    É imutável (frozen), então filtros, appenders e formatadores podem ler
    o mesmo evento sem risco de um alterar o que o outro vê.
    """

    message: str
    level: Level
    timestamp: datetime = field(default_factory=datetime.now)
