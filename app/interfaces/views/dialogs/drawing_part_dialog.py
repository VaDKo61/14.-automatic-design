from typing import Optional

from PySide6.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QPushButton


class FormatsButtonsDialog(QDialog):
    """Простой диалог выбора формата чертежа"""
    formats: tuple[str, str] = (
        'A3',
        'A2',
    )

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 400)
        self.selected: Optional[str] = None

        layout = QVBoxLayout(self)
        scroll = QScrollArea(widgetResizable=True)
        container = QWidget()
        vbox = QVBoxLayout(container)

        for form in FormatsButtonsDialog.formats:
            btn = QPushButton(form)
            btn.clicked.connect(lambda _, n=form: self._select(n))
            vbox.addWidget(btn)

        vbox.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _select(self, name: str) -> None:
        self.selected = name
        self.accept()

    @staticmethod
    def get_selection(title: str, parent=None) -> str:
        dlg = FormatsButtonsDialog(title, parent)
        return dlg.selected if dlg.exec() else None
