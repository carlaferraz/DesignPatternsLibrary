from pathlib import Path
from typing import Optional, Union

from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter
from minilog.core.logger import _check
from minilog.formatters.text import TextFormatter


class FileAppender(Appender):
    def __init__(
        self,
        path: Union[str, Path],
        formatter: Optional[Formatter] = None,
        encoding: str = "utf-8",
    ):
        super().__init__(_check(TextFormatter() if formatter is None else formatter, Formatter))
        self.path = Path(path)
        self.encoding = encoding

    def append(self, event: LogEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding=self.encoding) as file:
            file.write(self.formatter.format(event) + "\n")
