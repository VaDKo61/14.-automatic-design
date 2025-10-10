import re
import shutil

from pathlib import Path

from services.sw_utils import get_sw_app_and_model, SwError, assembly_verification

BASE_DIR: str = r'C:\SWR-Библиотеки 2021\Мое'


def get_list_files() -> list | None:
    path = Path(BASE_DIR)

    if not path.exists():
        return []

    return [f.name for f in path.iterdir() if f.is_file()]


def get_last_routing() -> dict[str, tuple[int, str, str]]:
    try:
        sw_app, sw_assem = get_sw_app_and_model()
    except SwError as e:
        raise SwError(str(e))

    try:
        assembly_verification(sw_assem)
    except SwError as e:
        raise SwError(str(e))

    last_routing: dict[str, tuple[int, str, str]] = {}
    for component in sw_assem.GetComponents(True):
        if component.Name2.startswith('БТП'):
            name_split: list[str] = re.split('[. ]', component.Name2.split('-')[0])
            if name_split[-1] == 'СБ':
                name_split.pop()
            name: str = '.'.join(name_split[3:-1])
            number: int = int(name_split[-1][-3::])

            if last_routing.get(name, (0, ''))[0] < number:
                last_routing[name] = (int(number), Path(component.GetPathName).name, component.Name2)

    return last_routing


def copy_template(selected_file: str, assem_dir: str, new_name_template: str) -> None:
    old_file = Path(BASE_DIR) / selected_file
    new_file_dir = Path(assem_dir)
    new_file = new_file_dir / new_name_template

    if new_file.exists():
        raise FileExistsError(f'Файл {new_name_template} уже существует, копирование пропущено')

    shutil.copy2(old_file, new_file)
