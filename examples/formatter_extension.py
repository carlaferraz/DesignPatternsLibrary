from minilog import Appender, Formatter, Level, LoggerBuilder
from minilog.formatters import ColorDecorator, FormatterDecorator, MaskDecorator, TextFormatter


class CsvFormatter(Formatter):
    def __init__(self, separator=";"):
        self.separator = separator

    def format(self, event):
        campos = [f"{event.timestamp:%H:%M:%S}", event.level.name, event.message]
        return self.separator.join(campos)


class PrefixDecorator(FormatterDecorator):
    def __init__(self, wrapped, prefix):
        super().__init__(wrapped)
        self.prefix = prefix

    def format(self, event):
        return f"{self.prefix} {self.wrapped.format(event)}"


class PrintAppender(Appender):
    def append(self, event):
        print(self.formatter.format(event))


pronto_da_lib = ColorDecorator(MaskDecorator(TextFormatter()))
feito_pelo_cliente = PrefixDecorator(MaskDecorator(CsvFormatter()), "[checkout]")

logger = (LoggerBuilder()
          .with_level(Level.INFO)
          .add_appender(PrintAppender(pronto_da_lib))
          .add_appender(PrintAppender(feito_pelo_cliente))
          .build())

logger.info("pedido criado")
logger.error("cartão 4111 1111 1111 1111 recusado, token=abc123")
