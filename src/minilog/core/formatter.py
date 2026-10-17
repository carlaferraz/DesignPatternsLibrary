from abc import ABC, abstractmethod

from minilog.core.event import LogEvent


class Formatter(ABC):
    @abstractmethod
    def format(self, event: LogEvent) -> str:
        ...
