from minilog.core.event import LogEvent
from minilog.core.level import Level
from minilog.filters.base import BaseFilter


class MinimumLevelFilter(BaseFilter):
    def __init__(self, minimum_level: Level):
        if not isinstance(minimum_level, Level):
            raise TypeError(f"esperava Level, recebeu {minimum_level!r}")
        self.minimum_level = minimum_level

    def matches(self, event: LogEvent) -> bool:
        return event.level >= self.minimum_level


class KeywordFilter(BaseFilter):
    def __init__(self, keyword: str):
        if not isinstance(keyword, str):
            raise TypeError(f"esperava str, recebeu {keyword!r}")
        if not keyword:
            raise ValueError("a palavra-chave não pode ser vazia")
        self.keyword = keyword.casefold()

    def matches(self, event: LogEvent) -> bool:
        return self.keyword in event.message.casefold()
