from datetime import datetime

from minilog.core import Level, LogEvent
from minilog.formatters import TextFormatter

EVENT = LogEvent("usuário entrou", Level.INFO, datetime(2026, 10, 29, 20, 30, 15))


def test_default_pattern_has_timestamp_level_and_message():
    assert TextFormatter().format(EVENT) == "2026-10-29 20:30:15 [INFO] usuário entrou"


def test_pattern_is_configurable():
    formatter = TextFormatter(pattern="{level}|{message}")
    assert formatter.format(EVENT) == "INFO|usuário entrou"


def test_time_format_is_configurable():
    formatter = TextFormatter(pattern="{timestamp}", time_format="%H:%M")
    assert formatter.format(EVENT) == "20:30"


def test_same_formatter_adapts_to_each_level():
    formatter = TextFormatter(pattern="{level}")
    levels = [formatter.format(LogEvent("x", level)) for level in Level]
    assert levels == ["DEBUG", "INFO", "WARNING", "ERROR"]
