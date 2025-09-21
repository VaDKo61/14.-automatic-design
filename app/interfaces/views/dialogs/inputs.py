from PySide6.QtWidgets import QInputDialog
from resources import strings as s


def ask_input_text(label: str) -> tuple[str, bool]:
    return QInputDialog.getText(
        None,
        s.BTN_CREATE_PROJECT,
        label
    )
