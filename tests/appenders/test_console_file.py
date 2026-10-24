import io
from datetime import datetime

import pytest

from minilog import Level, LogEvent, LoggerBuilder
from minilog.appenders import ConsoleAppender, FileAppender
from minilog.formatters import JsonFormatter, TextFormatter

MESSAGE_ONLY = TextFormatter(pattern="{level} {message}")
EVENT = LogEvent("usuário entrou", Level.INFO, datetime(2026, 10, 29, 20, 30, 15))


def test_console_writes_one_line_per_event_to_stdout(capsys):
    ConsoleAppender(MESSAGE_ONLY).append(EVENT)
    assert capsys.readouterr().out == "INFO usuário entrou\n"


def test_console_uses_text_formatter_by_default(capsys):
    ConsoleAppender().append(EVENT)
    assert capsys.readouterr().out == "2026-10-29 20:30:15 [INFO] usuário entrou\n"


def test_console_accepts_another_stream():
    stream = io.StringIO()
    ConsoleAppender(MESSAGE_ONLY, stream=stream).append(EVENT)
    assert stream.getvalue() == "INFO usuário entrou\n"


def test_file_appends_lines_and_creates_folders(tmp_path):
    path = tmp_path / "logs" / "app.log"
    appender = FileAppender(path, MESSAGE_ONLY)

    appender.append(EVENT)
    appender.append(LogEvent("caiu", Level.ERROR))

    assert path.read_text(encoding="utf-8") == "INFO usuário entrou\nERROR caiu\n"


def test_file_keeps_what_was_already_there(tmp_path):
    path = tmp_path / "app.log"
    path.write_text("antigo\n", encoding="utf-8")

    FileAppender(str(path), MESSAGE_ONLY).append(EVENT)

    assert path.read_text(encoding="utf-8") == "antigo\nINFO usuário entrou\n"


def test_formatter_can_be_swapped_without_changing_the_appender(tmp_path):
    path = tmp_path / "app.log"
    appender = FileAppender(path, MESSAGE_ONLY)
    appender.formatter = JsonFormatter()

    appender.append(EVENT)

    assert '"message": "usuário entrou"' in path.read_text(encoding="utf-8")


def test_same_log_reaches_console_and_file(tmp_path, capsys):
    path = tmp_path / "app.log"
    logger = (LoggerBuilder()
              .add_appender(ConsoleAppender(MESSAGE_ONLY))
              .add_appender(FileAppender(path, MESSAGE_ONLY))
              .build())

    logger.warning("disco cheio")

    assert capsys.readouterr().out == "WARNING disco cheio\n"
    assert path.read_text(encoding="utf-8") == "WARNING disco cheio\n"


def test_appenders_reject_anything_that_is_not_a_formatter(tmp_path):
    with pytest.raises(TypeError):
        ConsoleAppender(lambda event: event.message)
    with pytest.raises(TypeError):
        FileAppender(tmp_path / "app.log", "{message}")
