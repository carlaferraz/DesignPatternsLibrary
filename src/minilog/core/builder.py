from minilog.core.appender import Appender
from minilog.core.filter import Filter
from minilog.core.level import Level
from minilog.core.logger import DEFAULT_LEVEL, Logger, _check


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
        self._level = DEFAULT_LEVEL
        self._filters: list[Filter] = []
        self._appenders: list[Appender] = []

    def with_level(self, level: Level) -> "LoggerBuilder":
        self._level = _check(level, Level)
        return self

    def add_filter(self, log_filter: Filter) -> "LoggerBuilder":
        self._filters.append(_check(log_filter, Filter))
        return self

    def add_appender(self, appender: Appender) -> "LoggerBuilder":
        self._appenders.append(_check(appender, Appender))
        return self

    def build(self) -> Logger:
        if not self._appenders:
            raise ValueError("o logger precisa de pelo menos um appender")
        return Logger(self._level, self._filters, self._appenders)
