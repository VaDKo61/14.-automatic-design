from openpyxl.styles import PatternFill, Alignment, Side, Border


def create_style_excel(ws, matches: dict[str, list]) -> None:
    _edit_width_ws(ws)
    _add_headers(ws)

    blocks: tuple[tuple, ...] = (
        ('Совпадение на 100%', '548235', 'exact_matches'),
        ('Совпадение на 90%', 'A9D08E', 'fuzzy_matches'),
        ('Совпадение < 90%', 'C6E0B4', 'last_matches'),
    )

    for title, color, key in blocks:
        _add_subheader(ws, title, color)
        for rows in matches.get(key, []):
            for row in rows:
                ws.append(row)
            ws.append(('',))

    _add_fill_matches(ws)
    _add_alignment(ws)

    blocks_ast_items: tuple[tuple, ...] = (
        ('Оставшиеся позиции из Excel', 'spec', 'FFF2CC', 'E2EFDA'),
        ('Оставшиеся позиции из сборки', 'model_spec', 'BDD7EE', 'EBF1DE'),
        ('Фасонные части', 'secondary_items', 'BDD7EE', 'EBF1DE')
    )
    for block in blocks_ast_items:
        _add_remaining_section(ws, matches, *block)

    _add_borders_and_merge_empty(ws)


def _edit_width_ws(ws) -> None:
    widths = {
        'A': 30,
        'B': 7,
        'C': 7,
        'D': 8,
        'E': 200,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def _add_headers(ws) -> None:
    headers: tuple = (
        'Артикул',
        'Кол-во',
        'Совп.',
        'Ед. Изм.',
        'Наименование',
    )
    ws.append(headers)


def _add_subheader(ws, title: str, fill_color: str) -> None:
    cell = ws.cell(row=ws.max_row + 1, column=1, value=title)
    ws.merge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=5)
    _apply_fill(ws[cell.row], fill_color)


def _add_alignment(ws):
    alignments = {
        'left': ['A', 'E'],
        'center': ['B', 'C', 'D'],
    }

    for align, cols in alignments.items():
        for col in cols:
            for cell in ws[col]:
                cell.alignment = Alignment(horizontal=align, vertical='center')


def _add_fill_matches(ws) -> None:
    header = ws[1]
    _apply_fill(header, 'FFC000')  # Заголовок

    counter: int = 1
    for row in _get_cell(ws, min_row=3):
        name_cell = row[4]
        if name_cell.value is None:
            counter = 1
            continue

        color = 'BDD7EE' if counter == 2 else 'FFF2CC'
        _apply_fill(row, color)

        if counter == 2:
            continue
        _merge_row(ws, row[2].row)

        ws.cell(row=row[2].row, column=3).fill = _create_fill('92D050' if row[2].value == 0 else 'FF0000')
        counter += 1


def _add_remaining_section(ws, matches, title, key, fill, subheader_fill):
    if not matches.get(key):
        return
    ws.append(('',))
    _add_subheader(ws, title, subheader_fill)
    start_row = ws.max_row + 1
    for row in matches[key]:
        ws.append([row[0], row[1], row[2], '', row[3]])
    _fill_rows(ws, start_row, fill)


def _fill_rows(ws, start_row: int, fill_color: str):
    for row in ws.iter_rows(min_row=start_row):
        _apply_fill(row, fill_color)


def _apply_fill(row, rgb: str) -> None:
    for cell in row:
        cell.fill = _create_fill(rgb)


def _create_fill(rgb: str):
    return PatternFill(start_color=rgb, end_color=rgb, fill_type='solid')


def _merge_row(ws, row_idx: int) -> None:
    ws.merge_cells(start_row=row_idx, start_column=3, end_row=row_idx + 1, end_column=3)


def _add_borders_and_merge_empty(ws) -> None:
    thin = Side(border_style="thin", color="000000")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for row in _get_cell(ws):
        for cell in (cell for row in _get_cell(ws) for cell in row):
            cell.border = border
        if row[4].value is None:
            ws.merge_cells(start_row=row[0].row, start_column=1, end_row=row[0].row, end_column=5)


def _add_fill_last_items(ws, current_row: int, fill: str) -> None:
    for row in _get_cell(ws, min_row=current_row):
        _apply_fill(fill, row)


def _add_border(ws) -> None:
    thin = Side(border_style="thin", color="000000")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for cell in (cell for row in _get_cell(ws) for cell in row):
        cell.border = border


def _get_cell(
        ws,
        min_row: int = None,
        max_row: int = None,
        min_col: int = None,
        max_col: int = None,
        values_only: bool = False
):
    return list(ws.iter_rows(
        min_row=min_row,
        max_row=max_row,
        min_col=min_col,
        max_col=max_col,
        values_only=values_only
    ))
