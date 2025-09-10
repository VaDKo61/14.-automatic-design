from PySide6.QtWidgets import QMessageBox
from interfaces import ask_project_number
from resources import strings as s
from services import create_structure, show_success_with_link


def create_project_handle(main_window) -> None:
    project_number, ok = ask_project_number()

    if not ok:
        return None

    if not project_number or not project_number.isdigit():
        QMessageBox.warning(main_window, s.MSG_INPUT_WARNING_TITLE, s.MSG_INPUT_ERROR_CREATE_PROJECT)
        return None

    path = create_structure(project_number)
    if not path:
        QMessageBox.warning(main_window, s.MSG_INPUT_WARNING_TITLE, s.MSG_INPUT_ERROR_PROJECT_EXIST)
        return None

    show_success_with_link(main_window, path)
