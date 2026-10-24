import re
from typing import Dict, Iterable, Optional, Pattern

from minilog.core.event import LogEvent
from minilog.core.formatter import Formatter
from minilog.core.level import Level
from minilog.core.logger import _check

RESET = "\033[0m"
DEFAULT_COLORS = {
    Level.DEBUG: "\033[36m",
    Level.INFO: "\033[32m",
    Level.WARNING: "\033[33m",
    Level.ERROR: "\033[31m",
}

DEFAULT_MASK = "****"
CARD_NUMBER = re.compile(r"\b\d{4}(?:[ .-]?\d{4}){3}\b")
CPF = re.compile(r"\b\d{3}[. ]?\d{3}[. ]?\d{3}-?\d{2}\b")
SECRET = re.compile(r"(?P<keep>(?:senha|password|token|secret|api[_-]?key)\s*[=:]\s*)\S+", re.IGNORECASE)
DEFAULT_PATTERNS = (CARD_NUMBER, CPF, SECRET)


class FormatterDecorator(Formatter):
    def __init__(self, wrapped: Formatter):
        self.wrapped = _check(wrapped, Formatter)


class ColorDecorator(FormatterDecorator):
    def __init__(self, wrapped: Formatter, colors: Optional[Dict[Level, str]] = None):
        super().__init__(wrapped)
        self.colors = dict(DEFAULT_COLORS if colors is None else colors)

    def format(self, event: LogEvent) -> str:
        text = self.wrapped.format(event)
        color = self.colors.get(event.level)
        return f"{color}{text}{RESET}" if color else text


class MaskDecorator(FormatterDecorator):
    def __init__(
        self,
        wrapped: Formatter,
        patterns: Optional[Iterable[Pattern[str]]] = None,
        mask: str = DEFAULT_MASK,
    ):
        super().__init__(wrapped)
        self.patterns = tuple(DEFAULT_PATTERNS if patterns is None else patterns)
        self.mask = mask

    def format(self, event: LogEvent) -> str:
        text = self.wrapped.format(event)
        for pattern in self.patterns:
            text = pattern.sub(self._replace, text)
        return text

    def _replace(self, match: "re.Match[str]") -> str:
        keep = match.groupdict().get("keep")
        return f"{keep}{self.mask}" if keep else self.mask
