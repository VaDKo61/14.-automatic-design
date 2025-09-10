from pathlib import Path

BASE_PATH: str = r'D:\Solid Works\Проекты SW'


def create_structure(project_number: str) -> Path | None:
    path: Path = Path(BASE_PATH) / project_number
    if path.exists():
        return None
    path.mkdir(parents=True)

    folder: tuple = ('ИД',
                     r'КД/УВУ/Проверка',
                     r'КД/СО/Проверка',
                     r'КД/ГВС/Проверка',
                     'КД на печать',
                     'На согласование',
                     'СП')
    for name in folder:
        (path / name).mkdir(parents=True)

    return path
