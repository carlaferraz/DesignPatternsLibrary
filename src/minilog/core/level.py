from enum import IntEnum


class Level(IntEnum):
    """Níveis de log, do menos para o mais grave.

    Como é um IntEnum, dá para comparar direto: Level.ERROR > Level.INFO.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
