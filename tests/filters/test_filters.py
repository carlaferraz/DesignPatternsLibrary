import pytest

from minilog.core import Filter, Level, LogEvent
from minilog.filters import BaseFilter, FilterChain, KeywordFilter, MinimumLevelFilter


def event(message="pedido criado", level=Level.INFO):
    return LogEvent(message=message, level=level)


def test_minimum_level_filter_accepts_minimum_and_higher_levels():
    log_filter = MinimumLevelFilter(Level.WARNING)

    assert not log_filter.should_log(event(level=Level.INFO))
    assert log_filter.should_log(event(level=Level.WARNING))
    assert log_filter.should_log(event(level=Level.ERROR))


def test_keyword_filter_matches_case_insensitively():
    log_filter = KeywordFilter("PEDIDO")

    assert log_filter.should_log(event("Novo pedido criado"))
    assert not log_filter.should_log(event("usuário entrou"))


def test_filter_chain_stops_at_first_filter_that_rejects():
    visited = []

    class RecordingFilter(Filter):
        def __init__(self, result):
            self.result = result

        def should_log(self, log_event):
            visited.append(self.result)
            return self.result

    chain = FilterChain([RecordingFilter(False), RecordingFilter(True)])

    assert not chain.should_log(event())
    assert visited == [False]


def test_filter_chain_allows_event_when_every_filter_accepts():
    chain = FilterChain(
        [
            MinimumLevelFilter(Level.INFO),
            KeywordFilter("pedido"),
        ]
    )

    assert chain.should_log(event())
    assert not chain.should_log(event("usuário entrou"))


def test_filter_chain_is_a_filter_and_can_be_extended():
    class BlockKeywordFilter(BaseFilter):
        def matches(self, log_event):
            return "segredo" not in log_event.message.casefold()

    chain = FilterChain([MinimumLevelFilter(Level.INFO)])
    chain.add_filter(BlockKeywordFilter())

    assert chain.should_log(event("pedido criado"))
    assert not chain.should_log(event("pedido segredo"))


def test_invalid_filter_and_empty_keyword_are_rejected():
    with pytest.raises(TypeError):
        FilterChain([object()])
    with pytest.raises(ValueError):
        KeywordFilter("")
