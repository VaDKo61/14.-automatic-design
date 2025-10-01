from openpyxl.styles import PatternFill, Alignment


def get_cell(ws, min_row=None, max_row=None, min_col=None, max_col=None, values_only=False):
    return ws.iter_rows(
        min_row=min_row,
        max_row=max_row,
        min_col=min_col,
        max_col=max_col,
        values_only=values_only
    )


def add_headers(ws):
    headers: tuple = (
        'Артикул',
        'Кол-во',
        'Совп.',
        'Артикул',
        'Кол-во',
        'Наименование',
        'Наименование',
        'Поз.',
    )
    ws.append(headers)


def add_alignment(ws):
    for row in get_cell(ws):
        for cell in row:
            cell.alignment = Alignment(horizontal='left', vertical='center')

    for col in ['B', 'C', 'E', 'H']:
        for cell in ws[col]:
            cell.alignment = Alignment(horizontal='center', vertical='center')


def add_merge_row(ws_compare) -> int:
    row_merge: int = ws_compare.max_row + 1
    ws_compare.merge_cells(start_row=row_merge, start_column=1, end_row=row_merge, end_column=7)
    ws_compare.cell(row=row_merge, column=1, value='Нет совпадений')
    return row_merge


def edit_width_ws(ws):
    widths = {
        'A': 30,
        'B': 7,
        'C': 8,
        'D': 30,
        'E': 7,
        'F': 150,
        'G': 100,
        'H': 20,
    }

    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def create_fill(rgb):
    return PatternFill(start_color=rgb, end_color=rgb, fill_type='solid')


def add_fill(ws):
    header_fill = create_fill('FFC000')
    for cell in ws[1]:
        cell.fill = header_fill

    sp_fill = create_fill('FFF2CC')
    for row in get_cell(ws, min_col=1, max_col=2, min_row=2):
        for cell in row:
            cell.fill = sp_fill
    for row in get_cell(ws, min_col=6, max_col=6, min_row=2):
        for cell in row:
            cell.fill = sp_fill

    sp_assem_fill = create_fill('BDD7EE')
    for row in get_cell(ws, min_col=4, max_col=5, min_row=2):
        for cell in row:
            cell.fill = sp_assem_fill
    for row in get_cell(ws, min_col=7, max_col=7, min_row=2):
        for cell in row:
            cell.fill = sp_assem_fill

    ver_true_fill = create_fill('92D050')
    ver_false_fill = create_fill('FF0000')
    for row in get_cell(ws, min_col=3, max_col=3, min_row=2):
        for cell in row:
            cell.fill = ver_true_fill if cell.value == 0 else ver_false_fill
