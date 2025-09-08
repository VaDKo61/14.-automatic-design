from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QStatusBar, QMenuBar, QMenu, QMessageBox
)

from .dialogs import get_inputs_create_project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Помощник конструктора')
        self.resize(800, 600)
        self.setMinimumSize(400, 300)

        # Центральная часть окна
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.button_create_project = QPushButton('Создать новый проект')

        layout = QVBoxLayout()
        layout.addWidget(self.button_create_project, alignment=Qt.AlignTop)
        central_widget.setLayout(layout)

        # Статус-бар
        status = QStatusBar()
        self.setStatusBar(status)

        # Меню
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # Меню 'Файл'
        file_menu = QMenu('Файл', self)
        menu_bar.addMenu(file_menu)

        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню 'Помощь'
        help_menu = QMenu('Помощь', self)
        menu_bar.addMenu(help_menu)

        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Сигналы
        self.button_create_project.clicked.connect(self.handle_button_create_project)

    def handle_button_create_project(self):
        result = get_inputs_create_project()
        if result:
            number, title = result
            # result_text = process_result(number, text)
            # self.result_label.setText(result_text)
            # self.statusBar().showMessage('Ввод успешно выполнен', 3000)
        else:
            QMessageBox.warning(
                self,
                "Внимание",
                "Данные не были введены. Пожалуйста, заполните поля."
            )

    def show_about(self):
        QMessageBox.information(
            self,
            "О программе",
            "Приложение для конструктора Мегатрон\n\n"
            "Помощник конструктора\n"
            "(c) Вадим Морозов"
        )
