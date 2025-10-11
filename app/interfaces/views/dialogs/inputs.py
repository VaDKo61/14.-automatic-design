from PySide6.QtWidgets import QInputDialog
from resources import strings as s


def safe_ask_input_text(label: str) -> str | None:
    text, ok = ask_input_text(label)
    return text if ok and text.strip() else None


def ask_input_text(label: str) -> tuple[str, bool]:
    return QInputDialog.getText(
        None,
        s.BTN_CREATE_PROJECT,
        label
    )
