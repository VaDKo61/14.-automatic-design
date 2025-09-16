class ProjectError(Exception):
    """Базовое исключение для работы с проектами."""


class ProjectExistsError(ProjectError):
    """Проект уже существует."""


class InvalidProjectNumberError(ProjectError):
    """Некорректные данные."""
