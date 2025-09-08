import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from graphic_interfaces import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('graphic_interfaces/icons/Megatron.PNG'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()