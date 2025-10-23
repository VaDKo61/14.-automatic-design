from openpyxl.styles import PatternFill, Alignment, Side, Border


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
        'Ед. Изм.',
        'Совп.',
        'Наименование',
    )
    ws.append(headers)


def add_alignment(ws):
    alignments = {
        'left': ['A', 'D', 'E', 'F', 'G'],
        'center': ['B', 'C', 'E', 'H'],
    }

    for align, cols in alignments.items():
        for col in cols:
            for cell in ws[col]:
                cell.alignment = Alignment(horizontal=align, vertical='center')


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
        if isinstance(row, tuple):
            for cell in row:
                cell.fill = create_fill(fill)
        else:
            row.fill = create_fill(fill)


def add_merge_row(ws, row, value: str, fill: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
    cell = ws.cell(row=row, column=1, value=value)
    apply_fill(fill, (cell,))


def add_fill(ws):
    apply_fill('FFC000', get_cell(ws, min_col=1, min_row=1, max_row=1))  # Заголовок

    headers: list[str] = [
        'Фасонные части',
        'Оставшиеся позиции',
        'Совпадение < 90%',
        'Совпадение на 90%',
        'Совпадение на 100%',
    ]
    fill_headers: list[str] = ['EBF1DE', 'E2EFDA', 'C6E0B4', 'A9D08E', '548235']
    for row in get_cell(ws, min_row=2):
        if row[0].value == '-':
            add_merge_row(ws, row[0].row, headers[-1], fill_headers[-1])
            headers.pop()
            fill_headers.pop()
            continue
        apply_fill('FFF2CC', (row[0], row[1], row[5]))  # СП
        apply_fill('BDD7EE', (row[3], row[4], row[6]))  # СП сборки
        apply_fill('F2F2F2', (row[7],))  # Позиция
        if row[2].value == 0:
            apply_fill('92D050', (row[2],))
        else:
            apply_fill('FF0000', (row[2],))


def add_border(ws):
    thin = Side(border_style="thin", color="000000")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for cell in (cell for row in get_cell(ws) for cell in row):
        cell.border = border
