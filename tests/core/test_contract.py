from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from minilog.core import Appender, Filter, Formatter, Level, LogEvent


class UpperFormatter(Formatter):
    def format(self, event):
        return f"{event.level.name}: {event.message.upper()}"


class ListAppender(Appender):
    def __init__(self, formatter):
        super().__init__(formatter)
        self.lines = []

    def append(self, event):
        self.lines.append(self.formatter.format(event))


class OnlyErrors(Filter):
    def should_log(self, event):
        return event.level >= Level.ERROR


def test_levels_are_ordered():
    assert Level.DEBUG < Level.INFO < Level.WARNING < Level.ERROR


def test_event_gets_a_timestamp():
    event = LogEvent("oi", Level.INFO)
    assert event.message == "oi"
    assert event.level is Level.INFO
    assert isinstance(event.timestamp, datetime)


def test_event_is_immutable():
    event = LogEvent("oi", Level.INFO)
    with pytest.raises(FrozenInstanceError):
        event.message = "outra"


def test_abstract_classes_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Formatter()
    with pytest.raises(TypeError):
        Filter()
    with pytest.raises(TypeError):
        Appender(UpperFormatter())


def test_custom_components_work_together():
    appender = ListAppender(UpperFormatter())
    errors_only = OnlyErrors()

    for event in [LogEvent("tudo certo", Level.INFO), LogEvent("deu ruim", Level.ERROR)]:
        if errors_only.should_log(event):
            appender.append(event)

    assert appender.lines == ["ERROR: DEU RUIM"]
