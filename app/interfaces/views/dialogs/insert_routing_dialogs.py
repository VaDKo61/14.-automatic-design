from PySide6.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QPushButton
from typing import Optional

from .inputs import safe_ask_input_text


class ListButtonsDialog(QDialog):

    def __init__(
            self,
            items: list[str],
            title: str,
            list_type: str = '',
            parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 400)
        self.selected: Optional[str] = None

        layout = QVBoxLayout(self)
        scroll = QScrollArea(widgetResizable=True)
        container = QWidget()
        vbox = QVBoxLayout(container)

        for name in items:
            btn = QPushButton(name.split('.')[0] if list_type == 'Файлы' else name)
            btn.clicked.connect(lambda _, n=name: self._select(n))
            vbox.addWidget(btn)

        if list_type == 'Трубопроводы':
            new_btn = QPushButton('Ввести полное имя нового маршрута')
            new_btn.clicked.connect(lambda: self._input())
            vbox.addWidget(new_btn)

        vbox.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _select(self, name: str) -> None:
        self.selected = name
        self.accept()

    def _input(self) -> None:
        value = safe_ask_input_text('Введите полное имя шаблона')
        if not value:
            return
        self.selected = value
        self.accept()

    @staticmethod
    def get_selection(
            items: list[str],
            title: str,
            list_type: str = '',
            parent=None
    ) -> str:
        dlg = ListButtonsDialog(items, title, list_type, parent)
        return dlg.selected if dlg.exec() else None
