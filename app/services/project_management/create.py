import shutil
from pathlib import Path
from .errors import InvalidProjectNumberError, ProjectExistsError

BASE_PATH: str = r'D:\Solid Works\Проекты SW'
TEMPLATES_PATH: str = r'C:\SWR-Библиотеки 2021\Мое\Справка\Для проги'
TEMPLATE_FILES: list[Path] = [
    Path(TEMPLATES_PATH) / 'Замечания к БТП.docx',
    Path(TEMPLATES_PATH) / 'Чек-лист 3D.xlsm'
]
SUBFOLDERS: tuple[str, ...] = (
    'ИД',
    r'КД/УВУ/Проверка',
    r'КД/СО/Проверка',
    r'КД/ГВС/Проверка',
    'КД на печать',
    'На согласование',
    'СП',
    r'КД/УВУ/Проверка СП',
    r'КД/СО/Проверка СП',
    r'КД/ГВС/Проверка СП',
)
TARGET_FOLDERS: set[str] = {
    r'КД/УВУ/Проверка',
    r'КД/СО/Проверка',
    r'КД/ГВС/Проверка',
}


def create_structure(project_number: str) -> Path:
    """Создаёт структуру проекта с подкаталогами и копированием шаблонов."""

    if not project_number or not project_number.isdigit():
        raise InvalidProjectNumberError(
            'Данные не были введены или введены некорректно. '
            'Пожалуйста, заполните поля.'
        )

    project_path: Path = Path(BASE_PATH) / project_number
    if project_path.exists():
        raise ProjectExistsError(
            'Проект с таким номером уже существует. Пожалуйста, введите другой номер.'
        )

    project_path.mkdir()

    for folder in SUBFOLDERS:
        folder_path = project_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        if folder in TARGET_FOLDERS:
            _copy_templates_to_folder(folder_path, project_number)

    return project_path


def _copy_templates_to_folder(folder_path: Path, project_number: str) -> None:
    """Копирует все шаблоны в указанную папку с добавлением номера проекта."""

    for template_file in TEMPLATE_FILES:
        if template_file.exists():
            dest_file = folder_path / f'{template_file.stem} {project_number}{template_file.suffix}'
            shutil.copy(template_file, dest_file)
