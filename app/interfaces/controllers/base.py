import traceback

from abc import ABC, abstractmethod

from interfaces.views.messages import show_warning, show_error
from services.project_management import InvalidProjectNumberError, ProjectExistsError
from services.sw_utils import SwError, SwTableError
from services.sw_utils import SwTableError


class BaseUIHandler(ABC):
    """Базовый класс для всех UI-контроллеров."""

    def __init__(self, main_window):
        self.main_window = main_window

    def handle(self):
        try:
            self._execute()
        except (
                FileExistsError,
                SwError,
                InvalidProjectNumberError,
                ProjectExistsError,
                ValueError,
                FileNotFoundError,
        ) as e:
            show_warning(self.main_window, str(e))
        except Exception as e:
            traceback.print_exc()  # Отладка
            show_error(self.main_window, 'Критическая ошибка', str(e))

    @abstractmethod
    def _execute(self) -> None:
        pass
