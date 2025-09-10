from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from resources import strings as s


def setup_menu(main_window):
    menu_bar = QMenuBar()
    main_window.setMenuBar(menu_bar)

    # Файл
    file_menu = QMenu(s.MENU_FILE, main_window)
    exit_action = QAction(s.ACTION_EXIT, main_window)
    exit_action.triggered.connect(main_window.close)
    file_menu.addAction(exit_action)
    menu_bar.addMenu(file_menu)

    # Помощь
    help_menu = QMenu(s.MENU_HELP, main_window)
    about_action = QAction(s.ACTION_ABOUT, main_window)
    about_action.triggered.connect(main_window.show_about)
    help_menu.addAction(about_action)
    menu_bar.addMenu(help_menu)
