from interfaces.controllers import create_project_handle


def setup_signals(main_window):
    main_window.button_create_project.clicked.connect(
        lambda: create_project_handle(main_window)
    )