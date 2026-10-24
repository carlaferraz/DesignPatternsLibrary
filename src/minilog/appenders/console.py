import sys
from typing import Optional, TextIO

from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter
from minilog.core.logger import _check
from minilog.formatters.text import TextFormatter


class ConsoleAppender(Appender):
    def __init__(self, formatter: Optional[Formatter] = None, stream: Optional[TextIO] = None):
        super().__init__(_check(formatter or TextFormatter(), Formatter))
        self.stream = stream

    def append(self, event: LogEvent) -> None:
        stream = self.stream or sys.stdout
        stream.write(self.formatter.format(event) + "\n")
        stream.flush()
