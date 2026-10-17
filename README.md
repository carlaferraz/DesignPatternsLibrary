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

### Destinos (appenders)
(Carla)

### Filtros
(Gabi)

Referencias utilizadas:
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://medium.com/@dev.daniel.amorim/como-criar-biblioteca-python-pypi-343219656838