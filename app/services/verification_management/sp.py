from pathlib import Path

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from rapidfuzz import fuzz

from services.sw_utils.errors import SwTableError

# from .excel_utils import
from services.verification_management.excel_utils import *
from services.verification_management.matches import *

BASE_DIR_SP: str = 'Проверка СП'
TEMPLATE_DIR_SP_SW: str = r'C:\SWR-Библиотеки 2021\Мое\Справка\Для проги\Шаблон СП сборки.sldbomtbt'


def get_dir_sp(dir_project: str, number_project: str) -> str:
    dir_sp: Path = Path(dir_project).parent / BASE_DIR_SP
    if not dir_sp.exists():
        raise FileNotFoundError(f'Папка {dir_sp} не существует')

    for file in dir_sp.iterdir():
        if file.is_file():
            if number_project in file.stem:
                return str(file)
    else:
        raise FileNotFoundError(f'Специя с номером проекта {number_project} не найдена')


def save_sp_assem(sw_assem, dir_sp: str, number_project: str) -> str | None:
    sp_assem = sw_assem.Extension.InsertBomTable3(TEMPLATE_DIR_SP_SW, 0, 0, 1, 'По умолчанию', False, 0, False)
    if not sp_assem:
        raise SwTableError
    dir_sp_assem: Path = Path(dir_sp).parent / f'СП_{number_project}_SW.xlsx'
    sp_assem.SaveAsExcel(str(dir_sp_assem), False, False)
    sp_assem.BomFeature.GetFeature.Select2(False, 0)
    sw_assem.Extension.DeleteSelection2(1)
    return str(dir_sp_assem)


def verification_excel(
        ws_sp,
        ws_sp_assem
) -> tuple[list[tuple], list[tuple], list[tuple], list[tuple], list[tuple]]:
    values_sp: list[tuple] = [row for row in get_cell(ws_sp, min_col=1, max_col=5, min_row=3, values_only=True)]
    values_sp_assem: list[tuple] = [row for row in get_cell(ws_sp_assem, min_row=2, values_only=True)]

    exact_matches, values_sp_rest, values_sp_assem_rest = get_exact_matches(values_sp, values_sp_assem)

    fuzzy_matches, values_sp_rest, values_sp_assem_rest = get_fuzzy_matches(values_sp_rest, values_sp_assem_rest)

    matches_70, values_sp_rest, values_sp_assem_rest = match_items(values_sp_rest, values_sp_assem_rest, 70)
    matches_60, values_sp_rest, values_sp_assem_rest = match_items(values_sp_rest, values_sp_assem_rest, 60)
    matches_50, values_sp_rest, values_sp_assem_rest = match_items(values_sp_rest, values_sp_assem_rest, 50)
    last_matches: list[tuple] = [*matches_70, *matches_60, *matches_50]

    return exact_matches, fuzzy_matches, last_matches, values_sp_rest, values_sp_assem_rest


def save_verification_excel(dir_sp: str, dir_sp_assem: str):
    # wb_sp = load_workbook(dir_sp)
    # ws_sp = wb_sp.active
    #
    # wb_sp_assem = load_workbook(dir_sp_assem)
    # ws_sp_assem = wb_sp_assem.active

    wb_sp = load_workbook(r'C:\Users\Вадим\Desktop\Тестирование\8902\КД\Проверка СП\СП_8902.xlsx')
    ws_sp = wb_sp.active

    wb_sp_assem = load_workbook(r'C:\Users\Вадим\Desktop\Тестирование\8902\КД\Проверка СП\СП_8902_SW.xlsx')
    ws_sp_assem = wb_sp_assem.active

    (
        exact_matches,
        fuzzy_matches,
        last_matches,
        values_sp_rest,
        values_sp_assem_rest
    ) = verification_excel(ws_sp, ws_sp_assem)

    wb_compare = Workbook()
    ws_compare = wb_compare.active

    add_headers(ws_compare)
    for row in sorted(exact_matches, key=lambda x: x[2], reverse=True):
        ws_compare.append(row)
    merge_row: int = add_merge_row(ws_compare)
    for row in fuzzy_matches:
        ws_compare.append(row)
    merge_row_5: int = add_merge_row(ws_compare)
    for row in last_matches:
        ws_compare.append(row)
    merge_row_2: int = add_merge_row(ws_compare)
    for row in values_sp_rest:
        ws_compare.append(row)
    merge_row_3: int = add_merge_row(ws_compare)
    for row in values_sp_assem_rest:
        ws_compare.append(row)

    add_alignment(ws_compare)

    edit_width_ws(ws_compare)

    add_fill(ws_compare)

    # wb_compare.save(str(Path(dir_sp).parent / Path(dir_sp).name) + ' сравнение.xlsx')
    wb_compare.save(r'C:\Users\Вадим\Desktop\Тестирование\8902\КД\Проверка СП\СП_8902 сравнение.xlsx')


save_verification_excel('', '')
