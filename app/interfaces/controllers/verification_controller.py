from services.sw_utils import SwError
from services.verification_management import verification_sp
from interfaces.views.messages import show_warning

from .base import BaseUIHandler


class VerificationAssemSPHandler(BaseUIHandler):
    def _execute(self):
        verification_sp()
