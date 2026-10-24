# DesignPatternsLibrary
Repository for RA01 Design Patterns Subject

# minilog
Biblioteca extensível de logging e telemetria em Python, desenvolvida para a disciplina de Design Patterns.

## Integrantes
Carla Ferraz de Araujo,
Gabriella Tavares Pedroso,
Luiz Gustavo Santarosa,
Mateus Lima da Cruz,

## Vídeo de apresentação
//

## Instalação
```
pip install git+https://github.com/carlaferraz/DesignPatternsLibrary.git
```

Para desenvolver (com os testes):
```
pip install -e ".[dev]"
pytest
```

## Uso básico
```python
from minilog import LoggerBuilder, Level

logger = LoggerBuilder().with_level(Level.INFO).add_appender(meu_appender).build()
logger.info("usuário entrou")
```

## Como estender
Herde de `Formatter`, `Appender` ou `Filter` e entregue a peça ao `LoggerBuilder`, sem alterar a biblioteca. Exemplo completo em [examples/core_extension.py](examples/core_extension.py).


## Módulos

### Núcleo e configuração
(Mateus)

### Formatadores
(Luiz)

Um formatador transforma o `LogEvent` em texto e é trocável sem mexer no logger nem no appender (**Strategy**): `TextFormatter` para texto simples (padrão e formato de hora configuráveis) e `JsonFormatter` para JSON.
Os decoradores acrescentam comportamento a qualquer formatador, inclusive empilhados em qualquer combinação (**Decorator**): `ColorDecorator` colore a linha conforme o nível e `MaskDecorator` oculta cartão, CPF e trechos como `senha=` e `token=`.
Todo decorador também é um `Formatter`, então ele entra no appender no lugar do formatador original.

```python
from minilog.formatters import ColorDecorator, MaskDecorator, TextFormatter

formatter = ColorDecorator(MaskDecorator(TextFormatter()))
appender = MeuAppender(formatter)
```

Extensão (formatador CSV e decorador de prefixo criados pelo cliente, sem alterar a lib): [examples/formatter_extension.py](examples/formatter_extension.py)

### Destinos (appenders)
(Carla)

Um appender decide para onde o log vai e usa o seu `Formatter` para escrever: `ConsoleAppender` escreve no terminal e `FileAppender` acrescenta linhas em um arquivo.
O `Dispatcher` guarda uma lista de appenders e avisa todos a cada novo `LogEvent`, permitindo assinar e remover destinos mesmo com o logger já construído (**Observer**). Ele também é um `Appender`, então entra direto no `LoggerBuilder`.
A `AppenderFactory` cria o appender a partir de um nome (`"console"`, `"file"`) e aceita registrar nomes novos sem alterar a biblioteca (**Factory**).

```python
from minilog import LoggerBuilder
from minilog.appenders import AppenderFactory, Dispatcher

destinos = Dispatcher([AppenderFactory.create("console"), AppenderFactory.create("file", path="app.log")])
logger = LoggerBuilder().add_appender(destinos).build()
logger.info("aparece no console e no arquivo")
```

Extensão (appender em memória criado pelo cliente e registrado na fábrica, sem alterar a lib): [examples/appender_extension.py](examples/appender_extension.py)

### Filtros
(Gabi)

Referencias utilizadas:
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://medium.com/@dev.daniel.amorim/como-criar-biblioteca-python-pypi-343219656838