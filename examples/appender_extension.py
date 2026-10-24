from minilog import Appender, Level, LoggerBuilder
from minilog.appenders import AppenderFactory, Dispatcher
from minilog.formatters import JsonFormatter, TextFormatter


class MemoryAppender(Appender):
    def __init__(self, formatter=None):
        super().__init__(formatter or JsonFormatter())
        self.lines = []

    def append(self, event):
        self.lines.append(self.formatter.format(event))


AppenderFactory.register("memory", MemoryAppender)

console = AppenderFactory.create("console", formatter=TextFormatter())
arquivo = AppenderFactory.create("file", path="app.log")
memoria = AppenderFactory.create("memory")

destinos = Dispatcher([console, arquivo])

logger = (LoggerBuilder()
          .with_level(Level.INFO)
          .add_appender(destinos)
          .build())

logger.info("aparece no console e no arquivo")

destinos.subscribe(memoria)
logger.warning("agora também vai para a memória")

destinos.unsubscribe(console)
logger.error("só arquivo e memória")

print("disponíveis na fábrica:", AppenderFactory.available())
print("guardado em memória:", memoria.lines)
