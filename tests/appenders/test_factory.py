import pytest

from minilog import Appender
from minilog.appenders import AppenderFactory, ConsoleAppender, FileAppender
from minilog.formatters import JsonFormatter


class MemoryAppender(Appender):
    def __init__(self, formatter=None):
        super().__init__(formatter or JsonFormatter())
        self.lines = []

    def append(self, event):
        self.lines.append(self.formatter.format(event))


@pytest.fixture
def memory():
    AppenderFactory.register("memory", MemoryAppender)
    yield
    AppenderFactory.unregister("memory")


def test_builtin_names_create_the_right_appenders(tmp_path):
    assert isinstance(AppenderFactory.create("console"), ConsoleAppender)
    file_appender = AppenderFactory.create("file", path=tmp_path / "app.log")
    assert isinstance(file_appender, FileAppender)
    assert file_appender.path == tmp_path / "app.log"


def test_options_are_passed_to_the_appender():
    formatter = JsonFormatter()
    assert AppenderFactory.create("console", formatter=formatter).formatter is formatter


def test_names_ignore_case_and_spaces():
    assert isinstance(AppenderFactory.create("  Console "), ConsoleAppender)


def test_unknown_name_lists_the_available_ones():
    with pytest.raises(ValueError, match="console, file"):
        AppenderFactory.create("kafka")


def test_client_registers_a_new_appender_without_changing_the_lib(memory):
    appender = AppenderFactory.create("memory")
    assert isinstance(appender, MemoryAppender)
    assert "memory" in AppenderFactory.available()


def test_name_cannot_be_registered_twice_unless_replaced(memory):
    with pytest.raises(ValueError):
        AppenderFactory.register("memory", MemoryAppender)
    AppenderFactory.register("memory", lambda: MemoryAppender(), replace=True)
    assert isinstance(AppenderFactory.create("memory"), MemoryAppender)


def test_unregister_removes_the_name(memory):
    AppenderFactory.unregister("memory")
    assert "memory" not in AppenderFactory.available()
    AppenderFactory.register("memory", MemoryAppender)


def test_creator_must_build_an_appender():
    AppenderFactory.register("broken", lambda: "não sou appender")
    try:
        with pytest.raises(TypeError):
            AppenderFactory.create("broken")
    finally:
        AppenderFactory.unregister("broken")


def test_invalid_registrations_are_rejected():
    with pytest.raises(TypeError):
        AppenderFactory.register("x", "não é callable")
    with pytest.raises(ValueError):
        AppenderFactory.register("  ", MemoryAppender)
    with pytest.raises(KeyError):
        AppenderFactory.unregister("nunca registrado")
