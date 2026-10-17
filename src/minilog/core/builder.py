from minilog.core.appender import Appender
from minilog.core.filter import Filter
from minilog.core.level import Level
from minilog.core.logger import Logger


class LoggerBuilder:
    """Monta um Logger passo a passo (Builder).

    Cada método devolve o próprio builder, então dá para encadear:

        logger = (LoggerBuilder()
                  .with_level(Level.INFO)
                  .add_filter(meu_filtro)
                  .add_appender(meu_appender)
                  .build())
    """

    def __init__(self):
        self._level = Level.DEBUG
        self._filters: list[Filter] = []
        self._appenders: list[Appender] = []

    def with_level(self, level: Level) -> "LoggerBuilder":
        if not isinstance(level, Level):
            raise TypeError(f"nível inválido: {level!r}")
        self._level = level
        return self

    def add_filter(self, log_filter: Filter) -> "LoggerBuilder":
        if not isinstance(log_filter, Filter):
            raise TypeError(f"{log_filter!r} não é um Filter")
        self._filters.append(log_filter)
        return self

    def add_appender(self, appender: Appender) -> "LoggerBuilder":
        if not isinstance(appender, Appender):
            raise TypeError(f"{appender!r} não é um Appender")
        self._appenders.append(appender)
        return self

    def build(self) -> Logger:
        if not self._appenders:
            raise ValueError("o logger precisa de pelo menos um appender")
        return Logger(self._level, self._filters, self._appenders)
