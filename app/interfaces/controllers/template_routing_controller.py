from services import SwError, paste_template_routing, get_list_files


def get_list_files_for_ui() -> list[str]:
    return get_list_files()


def paste_template_routing_handle(main_window, selected_file: str) -> None:
    try:
        paste_template_routing()
    except SwError as e:
        print(e)
