from interfaces.controllers import create_project_handle
from interfaces.views.dialogs import show_file_buttons_dialog


def setup_signals(main_window):
    main_window.button_create_project.clicked.connect(
        lambda: create_project_handle(main_window)
    )

    main_window.button_paste_template_routing.clicked.connect(
        lambda: show_file_buttons_dialog(main_window)
    )
