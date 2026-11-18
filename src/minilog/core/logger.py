from typing import Iterable, Optional

from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.filter import Filter
from minilog.core.level import Level

DEFAULT_LEVEL = Level.DEBUG


class Logger:
    def __init__(
        self,
        level: Level = DEFAULT_LEVEL,
        filters: Optional[Iterable[Filter]] = None,
        appenders: Optional[Iterable[Appender]] = None,
    ):
        from minilog.appenders.dispatcher import Dispatcher
        from minilog.filters.chain import FilterChain

        self.level = _check(level, Level)
        self._filters = FilterChain(filters or [])
        self._dispatcher = Dispatcher(appenders or [])

    def debug(self, message: str) -> None:
        self.log(Level.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(Level.INFO, message)

    def warning(self, message: str) -> None:
        self.log(Level.WARNING, message)

    def error(self, message: str) -> None:
        self.log(Level.ERROR, message)

    def log(self, level: Level, message: str) -> None:
        if level < self.level:
            return
        event = LogEvent(message, level)
        if self._filters.should_log(event):
            self._dispatcher.notify(event)


def _check(value, expected_type):
    if not isinstance(value, expected_type):
        raise TypeError(f"esperava {expected_type.__name__}, recebeu {value!r}")
    return value
