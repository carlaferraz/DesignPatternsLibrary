from typing import Iterable, Optional

from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.filter import Filter
from minilog.core.level import Level

DEFAULT_LEVEL = Level.DEBUG


class Logger:
    """Fachada (Facade) da biblioteca.

    O cliente só chama logger.info("..."). Criar o LogEvent, checar o nível
    mínimo, passar pelos filtros e entregar para cada appender fica aqui
    dentro, escondido.
    """

    def __init__(
        self,
        level: Level = DEFAULT_LEVEL,
        filters: Optional[Iterable[Filter]] = None,
        appenders: Optional[Iterable[Appender]] = None,
    ):
        self.level = _check(level, Level)
        self._filters = [_check(f, Filter) for f in filters or []]
        self._appenders = [_check(a, Appender) for a in appenders or []]

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
        if self._passes_filters(event):
            self._dispatch(event)

    def _passes_filters(self, event: LogEvent) -> bool:
        return all(f.should_log(event) for f in self._filters)

    def _dispatch(self, event: LogEvent) -> None:
        for appender in self._appenders:
            appender.append(event)


def _check(value, expected_type):
    if not isinstance(value, expected_type):
        raise TypeError(f"esperava {expected_type.__name__}, recebeu {value!r}")
    return value
