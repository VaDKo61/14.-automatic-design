class SwError(Exception):
    """Базовое исключение для работы с SolidWorks"""

    def __init__(self, message: str | None = None):
        default_message = self.__class__.__doc__ or 'Неизвестная ошибка'
        super().__init__(message or default_message)


class SwAppError(SwError):
    """'SolidWorks не открыт."""


class SwModelError(SwError):
    """Нет активных окон"""


class SwAssemblyError(SwError):
    """Активна не сборка"""


class SwPartError(SwError):
    """Активна не деталь"""


class SwDrawingError(SwError):
    """Активен не чертеж"""


class SwTableError(SwError):
    """Спецификация не создана"""


class SwCreateDrawingError(SwError):
    """Чертеж не создан"""