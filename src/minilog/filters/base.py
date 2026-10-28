from abc import abstractmethod
from typing import final

from minilog.core.event import LogEvent
from minilog.core.filter import Filter


class BaseFilter(Filter):
    @final
    def should_log(self, event: LogEvent) -> bool:
        if not isinstance(event, LogEvent):
            raise TypeError(f"esperava LogEvent, recebeu {event!r}")
        return self.matches(event)

    @abstractmethod
    def matches(self, event: LogEvent) -> bool:
        """Return whether this event satisfies the filter's criterion."""
