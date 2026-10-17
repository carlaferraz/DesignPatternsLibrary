"""Exemplo de extensão: o cliente cria os próprios componentes.

Nada aqui altera a biblioteca. Basta herdar das classes do contrato
(Formatter, Appender, Filter) e entregar as peças ao LoggerBuilder.
"""

from minilog import Appender, Filter, Formatter, Level, LoggerBuilder


class BracketFormatter(Formatter):
    def format(self, event):
        return f"[{event.timestamp:%H:%M:%S}] [{event.level.name}] {event.message}"


class PrintAppender(Appender):
    def append(self, event):
        print(self.formatter.format(event))


class HideSecrets(Filter):
    def should_log(self, event):
        return "senha" not in event.message.lower()


logger = (LoggerBuilder()
          .with_level(Level.INFO)
          .add_filter(HideSecrets())
          .add_appender(PrintAppender(BracketFormatter()))
          .build())

logger.debug("não aparece: abaixo do nível mínimo")
logger.info("usuário entrou")
logger.warning("senha=123 não aparece: barrada pelo filtro")
logger.error("falha ao salvar o arquivo")
