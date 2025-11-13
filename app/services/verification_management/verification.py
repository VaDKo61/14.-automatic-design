from pathlib import Path

from .create_excel import create_verification_excel
from ..sw_utils.handler import SolidWorksHandler
from ..sw_utils.errors import SwTableError

BASE_DIR_SP: str = 'Проверка СП'
TEMPLATE_DIR_SP_SW: str = r'C:\SWR-Библиотеки 2021\Мое\Справка\Для проги\Шаблон СП сборки.sldbomtbt'


def verification_spec():
    with SolidWorksHandler() as sw:
        project_dir: str = sw.model.GetPathName

        project_number: str = Path(project_dir).stem.split('.')[1]

        spec_dir: str = _get_spec_dir(project_dir, project_number)

        model_spec_dir: str = _save_model_spec(sw.model, spec_dir, project_number)

        create_verification_excel(spec_dir, model_spec_dir)


def _get_spec_dir(dir_project: str, number_project: str) -> str:
    dir_sp: Path = Path(dir_project).parent / BASE_DIR_SP
    if not dir_sp.is_dir():
        raise FileNotFoundError(f'Папка не найдена: {dir_sp}')

    target_file = next(
        (
            file
            for file in dir_sp.iterdir()
            if file.is_file()
            and number_project in file.stem
            and not file.stem.lower().endswith('сравнение')
        ),
        None,
    )
    if not target_file:
        raise FileNotFoundError(f'Специя с номером проекта {number_project} не найдена')

    return str(target_file)


def _save_model_spec(model, dir_sp: str, number_project: str) -> str | None:
    bom_table = model.Extension.InsertBomTable3(
        TEMPLATE_DIR_SP_SW,
        0,
        0,
        1,
        'По умолчанию',
        False,
        0,
        False
    )
    if not bom_table:
        raise SwTableError

    bom_table.BomFeature.RoutingComponentGrouping = 2

    sort_data = bom_table.GetBomTableSortData
    sort_data.ColumnIndex(0, 3)
    sort_data.Ascending(0)
    sort_data.SortMethod = 0
    sort_data.ItemGroups = 0
    sort_data.DoNotChangeItemNumber = False
    sort_data.SaveCurrentSortParameters = True

    bom_table.Sort(sort_data)

    dir_sp_assem: Path = Path(dir_sp).parent / f'СП_{number_project}_SW.xlsx'

    bom_table.SaveAsExcel(str(dir_sp_assem), False, False)
    bom_table.BomFeature.GetFeature.Select2(False, 0)
    model.Extension.DeleteSelection2(1)
    return str(dir_sp_assem)
