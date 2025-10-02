from openpyxl.styles import PatternFill, Alignment


def get_cell(
        ws,
        min_row: int = None,
        max_row: int = None,
        min_col: int = None,
        max_col: int = None,
        values_only: bool = False
):
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
        'Артикул в сборке',
        'Кол-во',
        'Наименование',
        'Наименование в сборке',
        'Поз.',
    )
    ws.append(headers)


def add_alignment(ws):
    for col in ['A', 'D', 'E', 'F', 'G']:
        for cell in ws[col]:
            cell.alignment = Alignment(horizontal='left', vertical='center')

    for col in ['B', 'C', 'E', 'H']:
        for cell in ws[col]:
            cell.alignment = Alignment(horizontal='center', vertical='center')


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


def create_fill(rgb: str):
    return PatternFill(start_color=rgb, end_color=rgb, fill_type='solid')


def apply_fill(fill: str, rows: tuple):
    for row in rows:
        for cell in row:
            cell.fill = create_fill(fill)


def add_merge_row(ws) -> int:
    row_merge: int = ws.max_row + 1
    ws.merge_cells(start_row=row_merge, start_column=1, end_row=row_merge, end_column=7)
    ws.cell(row=row_merge, column=1, value='Нет совпадений')
    return row_merge


def add_fill(ws):
    apply_fill('FFC000', get_cell(ws, min_col=1, min_row=1, max_row=1))  # Заголовок

    for row in get_cell(ws, min_row=2):
        apply_fill('FFF2CC', ((row[0], row[1], row[5]),))
    # apply_fill(ws, sp_fill, 1, 2, min_row=2)
    # apply_fill(ws, sp_fill, 6, 6, min_row=2)
    #
    # sp_assem_fill = create_fill('BDD7EE')
    # apply_fill(ws, sp_assem_fill, 4, 5, min_row=2)
    # apply_fill(ws, sp_assem_fill, 7, 7, min_row=2)
    #
    # ver_true_fill = create_fill('92D050')
    # ver_false_fill = create_fill('FF0000')
    # for row in get_cell(ws, min_col=3, max_col=3, min_row=2):
    #     for cell in row:
    #         cell.fill = ver_true_fill if cell.value == 0 else ver_false_fill
