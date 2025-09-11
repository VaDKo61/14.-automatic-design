from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from resources import BUTTON_STYLE


class ButtonsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

    def add_button(self, text: str, width: int = 320, height: int = 50) -> QPushButton:
        button = QPushButton(text)
        button.setStyleSheet(BUTTON_STYLE)
        button.setFixedSize(width, height)
        self.layout.addWidget(button, alignment=Qt.AlignHCenter)
        return button
