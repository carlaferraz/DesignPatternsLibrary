from minilog import Level, LoggerBuilder
from minilog.appenders import ConsoleAppender
from minilog.filters import BaseFilter, FilterChain, KeywordFilter, MinimumLevelFilter
from minilog.formatters import TextFormatter


class BlockRepeatedMessages(BaseFilter):
    def __init__(self):
        self._last_message = None

    def matches(self, event):
        if event.message == self._last_message:
            return False
        self._last_message = event.message
        return True


filters = FilterChain(
    [
        MinimumLevelFilter(Level.INFO),
        KeywordFilter("pedido"),
        BlockRepeatedMessages(),
    ]
)

logger = (
    LoggerBuilder()
    .add_filter(filters)
    .add_appender(ConsoleAppender(TextFormatter()))
    .build()
)

logger.info("pedido confirmado")
logger.info("pedido confirmado")  # bloqueado pelo filtro do cliente
logger.warning("usuário entrou")  # bloqueado pelo filtro de palavra-chave
