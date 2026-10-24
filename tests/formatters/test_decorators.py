import json
import re
from datetime import datetime

import pytest

from minilog.core import Formatter, Level, LogEvent
from minilog.formatters import (
    ColorDecorator,
    FormatterDecorator,
    JsonFormatter,
    MaskDecorator,
    TextFormatter,
)
from minilog.formatters.decorators import RESET

MESSAGE_ONLY = TextFormatter(pattern="{message}")
EVENT = LogEvent("cartão 4111 1111 1111 1111", Level.WARNING, datetime(2026, 10, 29, 20, 30, 15))


def test_base_decorator_is_abstract():
    with pytest.raises(TypeError):
        FormatterDecorator(MESSAGE_ONLY)


def test_decorator_rejects_anything_that_is_not_a_formatter():
    with pytest.raises(TypeError):
        ColorDecorator(lambda event: event.message)


def test_color_wraps_the_decorated_output():
    decorated = ColorDecorator(MESSAGE_ONLY).format(EVENT)
    assert decorated == f"\033[33mcartão 4111 1111 1111 1111{RESET}"


def test_color_changes_with_the_level():
    formatter = ColorDecorator(MESSAGE_ONLY)
    colors = {formatter.format(LogEvent("x", level))[:5] for level in Level}
    assert len(colors) == 4


def test_level_without_a_color_stays_plain():
    formatter = ColorDecorator(MESSAGE_ONLY, colors={Level.ERROR: "\033[31m"})
    assert formatter.format(EVENT) == "cartão 4111 1111 1111 1111"


def test_mask_hides_card_numbers_cpf_and_secrets():
    event = LogEvent("cartão 4111-1111-1111-1111 cpf 123.456.789-01 senha=segredo123", Level.INFO)
    assert MaskDecorator(MESSAGE_ONLY).format(event) == "cartão **** cpf **** senha=****"


def test_mask_keeps_the_rest_of_the_line_untouched():
    event = LogEvent("pagamento aprovado", Level.INFO, datetime(2026, 10, 29, 20, 30, 15))
    assert MaskDecorator(TextFormatter()).format(event) == "2026-10-29 20:30:15 [INFO] pagamento aprovado"


def test_mask_patterns_and_symbol_are_configurable():
    formatter = MaskDecorator(MESSAGE_ONLY, patterns=[re.compile(r"\bbug\w*")], mask="[oculto]")
    event = LogEvent("bugfix urgente, senha=123", Level.INFO)
    assert formatter.format(event) == "[oculto] urgente, senha=123"


def test_decorators_stack_in_any_combination():
    masked_then_colored = ColorDecorator(MaskDecorator(MESSAGE_ONLY)).format(EVENT)
    colored_then_masked = MaskDecorator(ColorDecorator(MESSAGE_ONLY)).format(EVENT)
    assert masked_then_colored == f"\033[33mcartão ****{RESET}"
    assert colored_then_masked == f"\033[33mcartão ****{RESET}"


def test_decorators_work_over_any_strategy():
    payload = json.loads(MaskDecorator(JsonFormatter()).format(EVENT))
    assert payload["message"] == "cartão ****"


def test_decorator_is_a_formatter_so_it_fits_the_contract():
    assert isinstance(MaskDecorator(ColorDecorator(JsonFormatter())), Formatter)


def test_mask_applied_twice_is_stable():
    once = MaskDecorator(MESSAGE_ONLY)
    twice = MaskDecorator(once)
    assert twice.format(EVENT) == once.format(EVENT)
