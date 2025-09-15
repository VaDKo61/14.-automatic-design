import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton

from resources import strings as s


def show_info(main_window, title: str, text: str):
    QMessageBox.information(main_window, title, text)


def show_warning(main_window, text: str):
    QMessageBox.warning(main_window, s.MSG_INPUT_WARNING_TITLE, text)


def show_error(main_window, title: str, text: str):
    QMessageBox.critical(main_window, title, text)


def show_success_with_link(main_window, path) -> None:
    dialog = QDialog(main_window)
    dialog.setWindowTitle('Проект успешно создан')
    dialog.resize(500, 70)

    layout = QVBoxLayout()

    label = QLabel(
        f'{'Проект успешно создан'}\n'
        f'<a href="file:///{os.path.abspath(path)}">{path}</a>'
    )
    label.setTextFormat(Qt.RichText)
    label.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label.setOpenExternalLinks(True)

    ok_button = QPushButton('Oк')
    ok_button.clicked.connect(dialog.accept)

    layout.addWidget(label)
    layout.addWidget(ok_button, alignment=Qt.AlignHCenter)

    dialog.setLayout(layout)
    dialog.exec()
