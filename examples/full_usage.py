from pathlib import Path

from minilog import Level, LoggerBuilder
from minilog.appenders import AppenderFactory, Dispatcher
from minilog.filters import FilterChain, KeywordFilter, MinimumLevelFilter
from minilog.formatters import ColorDecorator, JsonFormatter, MaskDecorator, TextFormatter

Path("pedidos.log").unlink(missing_ok=True)

console = AppenderFactory.create("console", formatter=ColorDecorator(MaskDecorator(TextFormatter())))
arquivo = AppenderFactory.create("file", path="pedidos.log", formatter=MaskDecorator(JsonFormatter()))
filtros = FilterChain([MinimumLevelFilter(Level.INFO), KeywordFilter("pedido")])
logger = LoggerBuilder().add_filter(filtros).add_appender(Dispatcher([console, arquivo])).build()

logger.debug("pedido 41 em rascunho")
logger.info("pedido 42 criado")
logger.info("usuário abriu a página inicial")
logger.error("pedido 42 recusado: cartão 4111 1111 1111 1111")

print("\nconteúdo de pedidos.log:")
with open("pedidos.log", encoding="utf-8") as log:
    print(log.read())
