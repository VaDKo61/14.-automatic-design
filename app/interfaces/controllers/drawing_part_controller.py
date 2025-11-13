from services.drawing_part_management import create_draw

from .base import BaseUIHandler
from ..views.dialogs.drawing_part_dialog import FormatsButtonsDialog
from ..views.messages import show_info


class CreateDrawingPartHandler(BaseUIHandler):
    """Контроллер для создания чертежа детали"""

    def _execute(self):
        format_draw: str = FormatsButtonsDialog.get_selection('Выберите формат листа', self.main_window)
        create_draw(format_draw)
        # show_info(self.main_window, 'Выполнено', 'Спецификация сравнения создана')
