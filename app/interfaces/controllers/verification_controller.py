from services import SwError, verification_sp
from interfaces.views.messages import show_warning


def verification_sp_handle(main_window) -> None:
    try:
        verification_sp()
    except SwError as e:
        show_warning(main_window, str(e))
    except FileNotFoundError as e:
        show_warning(main_window, str(e))
