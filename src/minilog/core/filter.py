from abc import ABC, abstractmethod

from minilog.core.event import LogEvent


class Filter(ABC):
    @abstractmethod
    def should_log(self, event: LogEvent) -> bool:
        ...
