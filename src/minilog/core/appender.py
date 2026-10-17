from abc import ABC, abstractmethod

from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter


class Appender(ABC):
    def __init__(self, formatter: Formatter):
        self.formatter = formatter

    @abstractmethod
    def append(self, event: LogEvent) -> None:
        ...
