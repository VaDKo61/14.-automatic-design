import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from interfaces import MainWindow, setup_menu, setup_signals


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('resources/icons/Megatron.PNG'))
    window = MainWindow()

    setup_menu(window)
    setup_signals(window)

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
