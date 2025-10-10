from services import SwError, get_list_files, get_last_routing, insert_template_routing
from interfaces.views.messages import show_warning


def get_list_files_for_ui() -> list[str]:
    return get_list_files()


def get_current_routing_for_ui(main_window) -> dict[str, tuple[int, str, str]] | None:
    try:
        return get_last_routing()
    except SwError as e:
        show_warning(main_window, str(e))


def insert_template_routing_handle(main_window, selected_file: str, selected_routing: tuple[int, str]) -> None:
    try:
        insert_template_routing(selected_file, selected_routing)
    except FileExistsError as e:
        show_warning(main_window, str(e))
