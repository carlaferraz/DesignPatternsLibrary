import pytest

from minilog import Appender, Filter, Formatter, Level, Logger, LoggerBuilder


class PlainFormatter(Formatter):
    def format(self, event):
        return f"{event.level.name} {event.message}"


class ListAppender(Appender):
    def __init__(self):
        super().__init__(PlainFormatter())
        self.lines = []

    def append(self, event):
        self.lines.append(self.formatter.format(event))


class BlockWord(Filter):
    def __init__(self, word):
        self.word = word

    def should_log(self, event):
        return self.word not in event.message


# Logger (Facade)

def test_each_level_method_logs_with_its_level():
    out = ListAppender()
    logger = Logger(appenders=[out])

    logger.debug("a")
    logger.info("b")
    logger.warning("c")
    logger.error("d")

    assert out.lines == ["DEBUG a", "INFO b", "WARNING c", "ERROR d"]


def test_messages_below_min_level_are_dropped():
    out = ListAppender()
    logger = Logger(level=Level.WARNING, appenders=[out])

    logger.info("some")
    logger.warning("fica")

    assert out.lines == ["WARNING fica"]


def test_any_filter_can_block_the_event():
    out = ListAppender()
    logger = Logger(filters=[BlockWord("senha"), BlockWord("token")], appenders=[out])

    logger.info("login ok")
    logger.info("senha=123")
    logger.info("token=abc")

    assert out.lines == ["INFO login ok"]


def test_every_appender_receives_the_event():
    first, second = ListAppender(), ListAppender()
    logger = Logger(appenders=[first, second])

    logger.error("caiu")

    assert first.lines == second.lines == ["ERROR caiu"]


# LoggerBuilder (Builder)

def test_builder_chains_and_builds_a_working_logger():
    out = ListAppender()
    logger = (LoggerBuilder()
              .with_level(Level.INFO)
              .add_filter(BlockWord("senha"))
              .add_appender(out)
              .build())

    logger.debug("ignorado pelo nível")
    logger.info("senha=123")
    logger.info("chegou")

    assert out.lines == ["INFO chegou"]


def test_builder_requires_an_appender():
    with pytest.raises(ValueError):
        LoggerBuilder().build()


def test_builder_rejects_wrong_types():
    with pytest.raises(TypeError):
        LoggerBuilder().with_level("INFO")
    with pytest.raises(TypeError):
        LoggerBuilder().add_filter(lambda event: True)
    with pytest.raises(TypeError):
        LoggerBuilder().add_appender(print)


def test_loggers_from_the_same_builder_are_independent():
    out = ListAppender()
    builder = LoggerBuilder().add_appender(out)
    first = builder.build()
    builder.add_filter(BlockWord("x"))
    second = builder.build()

    first.info("x primeiro")
    second.info("x segundo")

    assert out.lines == ["INFO x primeiro"]


def test_logger_rejects_wrong_types_too():
    with pytest.raises(TypeError):
        Logger(level="INFO")
    with pytest.raises(TypeError):
        Logger(appenders=[print])
