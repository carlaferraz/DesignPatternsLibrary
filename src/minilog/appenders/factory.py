from typing import Callable, Dict, Tuple

from minilog.appenders.console import ConsoleAppender
from minilog.appenders.file import FileAppender
from minilog.core.appender import Appender

AppenderCreator = Callable[..., Appender]


class AppenderFactory:
    _creators: Dict[str, AppenderCreator] = {
        "console": ConsoleAppender,
        "file": FileAppender,
    }

    @classmethod
    def register(cls, name: str, creator: AppenderCreator, replace: bool = False) -> None:
        key = _normalize(name)
        if not callable(creator):
            raise TypeError(f"esperava um callable que crie um Appender, recebeu {creator!r}")
        if key in cls._creators and not replace:
            raise ValueError(f"já existe um appender registrado como '{key}'")
        cls._creators[key] = creator

    @classmethod
    def unregister(cls, name: str) -> None:
        key = _normalize(name)
        if key not in cls._creators:
            raise KeyError(f"nenhum appender registrado como '{key}'")
        del cls._creators[key]

    @classmethod
    def create(cls, name: str, **options) -> Appender:
        key = _normalize(name)
        if key not in cls._creators:
            available = ", ".join(cls.available())
            raise ValueError(f"appender desconhecido '{key}', disponíveis: {available}")
        appender = cls._creators[key](**options)
        if not isinstance(appender, Appender):
            raise TypeError(f"'{key}' deveria criar um Appender, criou {appender!r}")
        return appender

    @classmethod
    def available(cls) -> Tuple[str, ...]:
        return tuple(sorted(cls._creators))


def _normalize(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("o nome do appender precisa ser um texto não vazio")
    return name.strip().lower()
