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

O `Logger` é a fachada da biblioteca (**Facade**): recebe mensagens pelos métodos `debug`, `info`, `warning` e `error`, cria um `LogEvent` e coordena nível mínimo, filtros e destinos. Sem essa fachada, cada cliente precisaria montar e chamar esses componentes manualmente.
O `LoggerBuilder` permite montar a configuração por etapas — nível mínimo, filtros e appenders — e finalizá-la com `build()` (**Builder**). Assim, evitamos um construtor com muitos parâmetros opcionais e deixamos explícita a configuração escolhida.

```python
from minilog import Level, LoggerBuilder
from minilog.appenders import ConsoleAppender

logger = LoggerBuilder().with_level(Level.INFO).add_appender(ConsoleAppender()).build()
logger.info("usuário entrou")
```

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

Os filtros decidem se um `LogEvent` deve continuar sendo processado. `MinimumLevelFilter` aceita eventos a partir de um nível e `KeywordFilter` aceita mensagens que contenham uma palavra-chave, sem diferenciar maiúsculas de minúsculas.
A `FilterChain` executa os filtros em sequência e interrompe no primeiro que rejeitar o evento (**Chain of Responsibility**). A classe `BaseFilter` padroniza a validação e delega o critério para `matches`, que cada filtro concreto implementa (**Template Method**).

```python
from minilog import Level, LoggerBuilder
from minilog.filters import FilterChain, KeywordFilter, MinimumLevelFilter

filtros = FilterChain([MinimumLevelFilter(Level.INFO), KeywordFilter("pedido")])
logger = LoggerBuilder().add_filter(filtros).add_appender(meu_appender).build()
logger.info("pedido confirmado")
```

Extensão (filtro de mensagens repetidas criado pelo cliente, sem alterar a biblioteca): [examples/filter_extension.py](examples/filter_extension.py)

Referencias utilizadas:
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://medium.com/@dev.daniel.amorim/como-criar-biblioteca-python-pypi-343219656838