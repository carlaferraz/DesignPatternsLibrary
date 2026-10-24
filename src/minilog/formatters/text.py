from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter

DEFAULT_PATTERN = "{timestamp} [{level}] {message}"
DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class TextFormatter(Formatter):
    def __init__(self, pattern: str = DEFAULT_PATTERN, time_format: str = DEFAULT_TIME_FORMAT):
        self.pattern = pattern
        self.time_format = time_format

    def format(self, event: LogEvent) -> str:
        return self.pattern.format(
            timestamp=event.timestamp.strftime(self.time_format),
            level=event.level.name,
            message=event.message,
        )
