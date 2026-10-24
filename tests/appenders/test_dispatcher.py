import pytest

from minilog import Appender, Level, LogEvent, LoggerBuilder
from minilog.appenders import Dispatcher
from minilog.formatters import TextFormatter

EVENT = LogEvent("caiu", Level.ERROR)


class ListAppender(Appender):
    def __init__(self):
        super().__init__(TextFormatter(pattern="{level} {message}"))
        self.lines = []

    def append(self, event):
        self.lines.append(self.formatter.format(event))


def test_every_subscriber_receives_the_same_event():
    first, second = ListAppender(), ListAppender()
    dispatcher = Dispatcher([first, second])

    dispatcher.notify(EVENT)

    assert first.lines == second.lines == ["ERROR caiu"]


def test_unsubscribed_appender_stops_receiving():
    first, second = ListAppender(), ListAppender()
    dispatcher = Dispatcher().subscribe(first).subscribe(second)

    dispatcher.unsubscribe(first)
    dispatcher.notify(EVENT)

    assert first.lines == []
    assert second.lines == ["ERROR caiu"]


def test_same_appender_is_subscribed_only_once():
    out = ListAppender()
    dispatcher = Dispatcher().subscribe(out).subscribe(out)

    dispatcher.notify(EVENT)

    assert len(dispatcher) == 1
    assert out.lines == ["ERROR caiu"]


def test_unsubscribing_an_unknown_appender_is_harmless():
    dispatcher = Dispatcher()
    dispatcher.unsubscribe(ListAppender())
    assert dispatcher.appenders == ()


def test_dispatcher_rejects_invalid_subscribers():
    dispatcher = Dispatcher()
    with pytest.raises(TypeError):
        dispatcher.subscribe(print)
    with pytest.raises(ValueError):
        dispatcher.subscribe(dispatcher)


def test_subscribers_can_change_after_the_logger_is_built():
    first, late = ListAppender(), ListAppender()
    dispatcher = Dispatcher([first])
    logger = LoggerBuilder().add_appender(dispatcher).build()

    logger.info("antes")
    dispatcher.subscribe(late)
    logger.info("depois")

    assert first.lines == ["INFO antes", "INFO depois"]
    assert late.lines == ["INFO depois"]
