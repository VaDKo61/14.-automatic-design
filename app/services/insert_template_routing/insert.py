import re
from pathlib import Path

import pythoncom

from services.sw_utils import get_sw_app_and_model, create_com
from .files import copy_template


def create_new_name(selected_routing: tuple[int, str], selected_file: str) -> str:
    if selected_routing[0] == -1:
        return selected_routing[1] + Path(selected_file).suffix
    name_parts: list[str] = re.split('[. ]', selected_routing[1])

    index_number_routing: int = -2
    if name_parts[index_number_routing] == 'СБ':
        index_number_routing -= 1

    end_name: int = selected_routing[0] + 1
    name_parts[index_number_routing] = (str(end_name) if end_name >= 10 else '0' + str(end_name))

    return '.'.join(name_parts)


def get_coordinate_selected_routing(sw_assem, selected_routing: str) -> list[float]:
    comp_routing = sw_assem.GetComponentByName(selected_routing)
    return comp_routing.Transform2.ArrayData[9:12]


def insert_template_routing(selected_file: str, selected_routing: tuple[int, str]) -> None:
    sw_app, sw_assem = get_sw_app_and_model()

    assem_dir: str = sw_assem.GetPathName
    new_name_template: str = create_new_name(selected_routing, selected_file)

    try:
        copy_template(
            selected_file,
            '\\'.join(assem_dir.split('\\')[:-1]),
            new_name_template
        )
    except FileExistsError as e:
        raise FileExistsError(e)

    if selected_routing[0] == -1:
        coord_routing: list[float] = [0, 0, 0]
    else:
        coord_routing: list[float] = get_coordinate_selected_routing(sw_assem, selected_routing[2])

    arg1 = create_com(2, pythoncom.VT_BYREF | pythoncom.VT_I4)
    arg2 = create_com(128, pythoncom.VT_BYREF | pythoncom.VT_I4)
    doc_type: int = 2
    if new_name_template.lower().endswith('sldprt'):
        doc_type = 1
    for i in range(3):
        if sw_app.OpenDoc6(new_name_template, doc_type, 0, '', arg1, arg2):
            break
    sw_assem.AddComponent5(new_name_template, 0, '', False, '', *coord_routing)
    sw_app.CloseDoc(new_name_template)
