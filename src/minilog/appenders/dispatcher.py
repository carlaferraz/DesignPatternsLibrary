from typing import Iterable, List, Optional, Tuple

from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.logger import _check


class Dispatcher(Appender):
    def __init__(self, appenders: Optional[Iterable[Appender]] = None):
        super().__init__(None)
        self._appenders: List[Appender] = []
        for appender in appenders or []:
            self.subscribe(appender)

    @property
    def appenders(self) -> Tuple[Appender, ...]:
        return tuple(self._appenders)

    def subscribe(self, appender: Appender) -> "Dispatcher":
        _check(appender, Appender)
        if appender is self:
            raise ValueError("o dispatcher não pode assinar a si mesmo")
        if appender not in self._appenders:
            self._appenders.append(appender)
        return self

    def unsubscribe(self, appender: Appender) -> "Dispatcher":
        if appender in self._appenders:
            self._appenders.remove(appender)
        return self

    def notify(self, event: LogEvent) -> None:
        for appender in list(self._appenders):
            appender.append(event)

    def append(self, event: LogEvent) -> None:
        self.notify(event)

    def __len__(self) -> int:
        return len(self._appenders)
