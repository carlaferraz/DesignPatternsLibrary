from abc import ABC, abstractmethod

from minilog.core.event import LogEvent


class Filter(ABC):
    """Decide se um evento deve seguir adiante ou ser descartado."""

    @abstractmethod
    def should_log(self, event: LogEvent) -> bool:
        ...
