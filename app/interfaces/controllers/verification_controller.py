from services.verification_management import verification_spec

from .base import BaseUIHandler


class VerificationAssemSPHandler(BaseUIHandler):
    """Контроллер для проверки сборки со спецификацией."""

    def _execute(self):
        verification_spec()
