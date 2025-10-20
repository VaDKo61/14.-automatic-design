import re
import shutil

from pathlib import Path

from ..sw_utils.handler import SolidWorksHandler

BASE_DIR: Path = Path(r'C:\SWR-Библиотеки 2021\Мое')


def get_list_files() -> list:
    if not BASE_DIR.exists():
        raise FileNotFoundError(f'Папка с шаблонами не найдена: {BASE_DIR}')

    return [f.name for f in BASE_DIR.iterdir() if f.is_file()]


def get_current_routing() -> dict[str, tuple[int, str, str]]:
    with SolidWorksHandler() as sw:
        sw.verify_assembly()

        latest_routing: dict[str, tuple[int, str, str]] = {}
        components = sw.model.GetComponents(True)
        if not components:
            return {}

        for component in components:
            comp_name = component.Name2

            if not comp_name.startswith('БТП'):
                continue

            name_split: list[str] = re.split('[. ]', component.Name2.split('-')[0])

            if name_split[-1] == 'СБ':
                name_split.pop()

            try:
                name: str = '.'.join(name_split[3:-1])
                number: int = int(name_split[-1][-3::])
            except (IndexError, ValueError):
                continue

            comp_path = Path(component.GetPathName)

            prev_number, *_ = latest_routing.get(name, (0, '', ''))
            if number > prev_number:
                latest_routing[name] = (number, comp_path.name, comp_name)

        return latest_routing


def copy_template(selected_file: str, assem_dir: str, new_name_template: str) -> None:
    old_file = BASE_DIR / selected_file
    new_file = Path(assem_dir) / new_name_template

    if new_file.exists():
        raise FileExistsError(
            f'Файл {new_name_template} уже существует, копирование пропущено'
        )

    shutil.copy2(old_file, new_file)
