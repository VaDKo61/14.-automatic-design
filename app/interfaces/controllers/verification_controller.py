from services.verification_management import verification_spec

from .base import BaseUIHandler
from ..views.messages import show_info


class VerificationAssemSPHandler(BaseUIHandler):
    """Контроллер для проверки сборки со спецификацией."""

    def _execute(self):
        verification_spec()
        show_info(self.main_window, 'Выполнено', 'Спецификация сравнения создана')
