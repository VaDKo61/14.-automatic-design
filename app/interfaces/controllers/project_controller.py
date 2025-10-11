from services.project_management import create_structure

from .base import BaseUIHandler
from ..views.messages import show_success_with_link
from ..views.dialogs.inputs import ask_input_text


class CreateProjectHandler(BaseUIHandler):
    """Контроллер для создания структуры проекта"""

    def _execute(self):
        project_number, ok = ask_input_text('Введите номер заказа:')
        if not ok:
            return

        path = create_structure(project_number)
        show_success_with_link(self.main_window, path)
