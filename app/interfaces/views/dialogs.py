from PySide6.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QPushButton

from interfaces.controllers import get_list_files_for_ui, get_current_routing_for_ui, insert_template_routing_handle

from .messages import show_warning


class ListButtonsDialog(QDialog):
    def __init__(self, name_buttons: list[str], message: str, name_list: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(message)
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.buttons_layout = QVBoxLayout(container)
        scroll.setWidget(container)

        layout.addWidget(scroll)

        self.selected_buttons: str | None = None
        self.render_buttons(name_buttons, name_list)

    def render_buttons(self, buttons: list[str], name_list: str):
        if not buttons:
            show_warning(self, f'{name_list} не найдены')
            self.close()
            return

        for button_name in buttons:
            btn = QPushButton(button_name)
            if name_list == 'Файлы':
                btn = QPushButton(button_name.split('.')[0])
            btn.clicked.connect(lambda checked, f=button_name: self.handle_file_click(f))
            self.buttons_layout.addWidget(btn)

        self.buttons_layout.addStretch()

    def handle_file_click(self, buttons_name: str):
        self.selected_buttons = buttons_name
        self.accept()


def show_file_routing_buttons_dialog(main_window):
    files: list[str] = get_list_files_for_ui()
    if not files:
        show_warning(main_window, 'Файлы не найдены')
        return
    dialog_files = ListButtonsDialog(files, 'Выберите шаблон', 'Файлы', main_window)

    if dialog_files.exec() == QDialog.Accepted and dialog_files.selected_buttons:
        current_routing: dict[str, tuple[int, str]] = get_current_routing_for_ui(main_window)
        if not current_routing:
            return

    dialog_routing = ListButtonsDialog(
        list(current_routing.keys()),
        'Выберите трубопровод, который продолжим',
        'Трубопроводы',
        main_window
    )

    if dialog_routing.exec() == QDialog.Accepted and dialog_files.selected_buttons:
        insert_template_routing_handle(
            main_window,
            dialog_files.selected_buttons,
            current_routing[dialog_routing.selected_buttons]
        )
