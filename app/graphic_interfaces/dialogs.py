from PySide6.QtWidgets import QInputDialog


def get_inputs_create_project() -> tuple[int, str] | None:
    number, ok1 = QInputDialog.getInt(
        None,
        'Создать новый проект',
        'Введите номер заказа:',
        value=1,
        minValue=1,
        maxValue=10000,
        step=1
    )
    if not ok1:
        return None

    title, ok2 = QInputDialog.getText(
        None,
        'Создать новый проект',
        'Введите название объекта:'
    )
    if not ok2 or not title:
        return None

    return number, title
