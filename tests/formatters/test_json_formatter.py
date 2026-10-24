import json
from datetime import datetime

from minilog.core import Level, LogEvent
from minilog.formatters import JsonFormatter, TextFormatter

EVENT = LogEvent("usuário entrou", Level.ERROR, datetime(2026, 10, 29, 20, 30, 15))


def test_output_is_valid_json_with_the_event_fields():
    payload = json.loads(JsonFormatter().format(EVENT))
    assert payload == {
        "timestamp": "2026-10-29T20:30:15",
        "level": "ERROR",
        "message": "usuário entrou",
    }


def test_accents_are_not_escaped():
    assert "usuário" in JsonFormatter().format(EVENT)


def test_indent_and_sort_keys_are_configurable():
    output = JsonFormatter(indent=2, sort_keys=True).format(EVENT)
    assert output.startswith('{\n  "level"')


def test_strategies_are_interchangeable_for_the_same_event():
    outputs = {formatter.format(EVENT) for formatter in (TextFormatter(), JsonFormatter())}
    assert len(outputs) == 2
