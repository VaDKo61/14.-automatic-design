import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from resources import strings as s


def show_success_with_link(main_window, path) -> None:
    msg = QMessageBox(main_window)
    msg.setWindowTitle(s.MSG_CREATE_PROJECT)
    msg.setIcon(QMessageBox.Information)

    msg.setText(
        f'{s.MSG_CREATE_PROJECT}\n'
        f'<a href="file:///{os.path.abspath(path)}">{path}</a>'
    )
    msg.setTextFormat(Qt.RichText)
    msg.setTextInteractionFlags(Qt.TextBrowserInteraction)

    msg.setMinimumWidth(800)
    msg.setMinimumHeight(200)

    msg.exec()
