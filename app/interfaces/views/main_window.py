from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar
from PySide6.QtCore import Qt

from resources import strings as s

from .messages import show_info
from .buttons_panel import ButtonsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(s.APP_TITLE)
        self.resize(800, 600)
        self.setMinimumSize(400, 300)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.buttons_panel = ButtonsPanel()

        self.button_create_project = (
            self.buttons_panel.add_button(s.BTN_CREATE_PROJECT)
        )
        self.button_verification_project = (
            self.buttons_panel.add_button(s.BTN_VERIFICATION_PROJECT)
        )
        self.button_paste_template_routing = (
            self.buttons_panel.add_button(s.BTN_PASTE_TEMPLATE_ROUTING)
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addStretch()
        layout.addWidget(self.buttons_panel, alignment=Qt.AlignCenter)
        layout.addStretch()
        central_widget.setLayout(layout)

        self.setStatusBar(QStatusBar())

    def show_about(self):
        show_info(self, s.APP_ABOUT_TITLE, s.APP_ABOUT_TEXT)
