from PySide6.QtWidgets import QMessageBox
from interfaces import ask_project_number
from resources import strings as s
from services import create_structure, show_success_with_link, InvalidProjectNumberError, ProjectExistsError


def create_project_handle(main_window) -> None:
    project_number, ok = ask_project_number()

    if not ok:
        return None

    try:
        path = create_structure(project_number)
        show_success_with_link(main_window, path)
    except InvalidProjectNumberError as e:
        QMessageBox.warning(main_window, s.MSG_INPUT_WARNING_TITLE, s.MSG_INPUT_ERROR_CREATE_PROJECT)
    except ProjectExistsError as e:
        QMessageBox.warning(main_window, s.MSG_INPUT_WARNING_TITLE, s.MSG_INPUT_ERROR_PROJECT_EXIST)
    except Exception as e:
        QMessageBox.critical(main_window, 'Критическая ошибка', str(e))


def paste_template_routing(main_window):
    pass
