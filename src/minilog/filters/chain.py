from typing import Iterable, Tuple

from minilog.core.event import LogEvent
from minilog.core.filter import Filter


class FilterChain(Filter):
    def __init__(self, filters: Iterable[Filter] = ()):
        self._filters: list[Filter] = []
        for log_filter in filters:
            self.add_filter(log_filter)

    @property
    def filters(self) -> Tuple[Filter, ...]:
        return tuple(self._filters)

    def add_filter(self, log_filter: Filter) -> "FilterChain":
        if not isinstance(log_filter, Filter):
            raise TypeError(f"esperava Filter, recebeu {log_filter!r}")
        if log_filter is self:
            raise ValueError("a cadeia não pode conter a si mesma")
        self._filters.append(log_filter)
        return self

    def should_log(self, event: LogEvent) -> bool:
        for log_filter in self._filters:
            if not log_filter.should_log(event):
                return False
        return True
