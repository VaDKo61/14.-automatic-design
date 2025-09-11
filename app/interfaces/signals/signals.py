from interfaces.controllers import create_project_handle, paste_template_routing


def setup_signals(main_window):
    main_window.button_create_project.clicked.connect(
        lambda: create_project_handle(main_window)
    )

    main_window.button_paste_template_routing.clicked.connect(
        lambda: paste_template_routing(main_window)
    )