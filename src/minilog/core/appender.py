from abc import ABC, abstractmethod

from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter


class Appender(ABC):
    """Destino de um log (console, arquivo, ...).

    Cada appender recebe o seu Formatter e o usa em append() para
    transformar o evento em texto antes de escrever.
    """

    def __init__(self, formatter: Formatter):
        self.formatter = formatter

    @abstractmethod
    def append(self, event: LogEvent) -> None:
        ...
