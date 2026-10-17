from abc import ABC, abstractmethod

from minilog.core.event import LogEvent


class Formatter(ABC):
    """Transforma um LogEvent no texto que vai ser escrito."""

    @abstractmethod
    def format(self, event: LogEvent) -> str:
        ...
