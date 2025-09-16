from PySide6.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QPushButton

from interfaces.controllers import get_list_files_for_ui, paste_template_routing_handle

from .messages import show_warning


class FileButtonsDialog(QDialog):
    def __init__(self, files: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle('Выберите шаблон')
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.buttons_layout = QVBoxLayout(container)
        scroll.setWidget(container)

        layout.addWidget(scroll)

        self.selected_file: str | None = None
        self.render_buttons(files)

    def render_buttons(self, files: list[str]):
        if not files:
            show_warning(self, 'Файлы не найдены')
            self.close()
            return

        for file_name in files:
            btn = QPushButton(file_name)
            btn.clicked.connect(lambda checked, f=file_name: self.handle_file_click(f))
            self.buttons_layout.addWidget(btn)

        self.buttons_layout.addStretch()

    def handle_file_click(self, file_name: str):
        self.selected_file = file_name
        self.accept()


def show_file_buttons_dialog(main_window):
    files = get_list_files_for_ui()
    if not files:
        show_warning(main_window, 'Файлы не найдены')
        return

    dialog = FileButtonsDialog(files, main_window)
    if dialog.exec() == QDialog.Accepted and dialog.selected_file:
        paste_template_routing_handle(main_window, dialog.selected_file)
