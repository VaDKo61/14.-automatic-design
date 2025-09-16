from pathlib import Path

BASE_DIR: str = r'C:\SWR-Библиотеки 2021\Мое'


def get_list_files() -> list | None:
    path = Path(BASE_DIR)

    if not path.exists():
        return []

    return [f.name for f in path.iterdir() if f.is_file()]
