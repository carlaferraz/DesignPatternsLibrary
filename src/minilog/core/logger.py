from minilog.core.appender import Appender
from minilog.core.event import LogEvent
from minilog.core.filter import Filter
from minilog.core.level import Level


class Logger:
    """Fachada (Facade) da biblioteca.

    O cliente só chama logger.info("..."). Criar o LogEvent, checar o nível
    mínimo, passar pelos filtros e entregar para cada appender fica aqui
    dentro, escondido.
    """

    def __init__(self, level=Level.DEBUG, filters=None, appenders=None):
        self.level = level
        self._filters: list[Filter] = list(filters or [])
        self._appenders: list[Appender] = list(appenders or [])

    def debug(self, message: str) -> None:
        self.log(Level.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(Level.INFO, message)

    def warning(self, message: str) -> None:
        self.log(Level.WARNING, message)

    def error(self, message: str) -> None:
        self.log(Level.ERROR, message)

    def log(self, level: Level, message: str) -> None:
        if level < self.level:
            return
        event = LogEvent(message, level)
        if self._passes_filters(event):
            self._dispatch(event)

    # Os dois métodos abaixo são onde entram a FilterChain e o Dispatcher
    # quando ficarem prontos. Trocar o miolo deles não muda nada para quem
    # usa o Logger.

    def _passes_filters(self, event: LogEvent) -> bool:
        return all(f.should_log(event) for f in self._filters)

    def _dispatch(self, event: LogEvent) -> None:
        for appender in self._appenders:
            appender.append(event)
