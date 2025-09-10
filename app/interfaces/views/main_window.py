from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStatusBar, QMessageBox
from PySide6.QtCore import Qt
from resources import strings as s


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

        self.button_create_project = QPushButton(s.BTN_CREATE_PROJECT)

        layout = QVBoxLayout()
        layout.addWidget(self.button_create_project, alignment=Qt.AlignTop)
        central_widget.setLayout(layout)

        self.setStatusBar(QStatusBar())

    def show_about(self):
        QMessageBox.information(self, s.APP_ABOUT_TITLE, s.APP_ABOUT_TEXT)
