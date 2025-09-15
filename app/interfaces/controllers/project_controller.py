from interfaces import ask_project_number
from services import create_structure, InvalidProjectNumberError, ProjectExistsError
from interfaces.views import show_success_with_link, show_warning, show_error


def create_project_handle(main_window) -> None:
    project_number, ok = ask_project_number()

    if not ok:
        return None

    try:
        path = create_structure(project_number)
        show_success_with_link(main_window, path)
    except InvalidProjectNumberError as e:
        show_warning(main_window, str(e))
    except ProjectExistsError as e:
        show_warning(main_window, str(e))
    except Exception as e:
        show_error(main_window, 'Критическая ошибка', str(e))


def paste_template_routing(main_window):
    pass
