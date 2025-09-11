import shutil
from pathlib import Path

BASE_PATH: str = r'D:\Solid Works\Проекты SW'
TEMPLATES_PATH: str = r'C:\SWR-Библиотеки 2021\Мое\Справка\Для проги'
TEMPLATE_FILES: list[Path] = [
    Path(TEMPLATES_PATH) / 'Замечания к БТП.docx',
    Path(TEMPLATES_PATH) / 'Чек-лист 3D.xlsm'
]


def create_structure(project_number: str) -> Path | None:
    path: Path = Path(BASE_PATH) / project_number
    if path.exists():
        return None
    path.mkdir()

    subfolders: tuple = (
        'ИД',
        r'КД/УВУ/Проверка',
        r'КД/СО/Проверка',
        r'КД/ГВС/Проверка',
        'КД на печать',
        'На согласование',
        'СП'
    )
    target_folders: set = {
        r'КД/УВУ/Проверка',
        r'КД/СО/Проверка',
        r'КД/ГВС/Проверка',
    }

    for folder in subfolders:
        folder_path = (path / folder)
        folder_path.mkdir(parents=True)
        if folder in target_folders:
            for template_file in TEMPLATE_FILES:
                if template_file.exists():
                    shutil.copy(template_file, folder_path / template_file.name)

    return path
