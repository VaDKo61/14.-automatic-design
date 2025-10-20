from services.insert_template_routing import get_list_files, get_current_routing, insert_template_routing

from .base import BaseUIHandler
from ..views.dialogs.insert_routing_dialogs import ListButtonsDialog


class InsertTemplateRoutingHandler(BaseUIHandler):
    """Контроллер для вставки шаблона маршрута."""

    def _execute(self):
        selected_file: str = self._select_template_file()
        if not selected_file:
            return

        current_routing: dict[str, tuple[int, str, str]] = get_current_routing() or {}

        selected_routing = self._select_routing(current_routing)

        insert_template_routing(selected_file, selected_routing)

    def _select_template_file(self) -> str:
        """Показывает диалог выбора шаблона."""

        files: list[str] = get_list_files()
        if not files:
            raise FileExistsError('Шаблоны не найдены')

        return ListButtonsDialog.get_selection(
            files,
            'Выберите шаблон',
            'Файлы',
            self.main_window
        )

    def _select_routing(self, current_routing: dict[str, tuple[int, str, str]]) -> tuple[int, str, str]:
        """Показывает диалог выбора маршрута (существующего или нового)."""

        selected_routing = ListButtonsDialog.get_selection(
            sorted(current_routing.keys()),
            'Выберите трубопровод, который продолжим',
            'Трубопроводы',
            self.main_window,
        )
        if not selected_routing:
            raise ValueError('Имя пустое')

        return current_routing.get(selected_routing, (-1, selected_routing))
