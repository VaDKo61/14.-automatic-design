from pathlib import Path

import pythoncom

from services.sw_utils import get_sw_app_and_model, create_com
from .files import copy_template
from ..sw_utils.connection import SolidWorksHandler


def create_new_name(selected_routing: tuple[int, str], selected_file: str) -> str:
    if selected_routing[0] == -1:
        return selected_routing[1] + Path(selected_file).suffix
    name_parts: list[str] = selected_routing[1].split('.')

    end_name: int = selected_routing[0] + 1
    name_parts[-2] = f'{(str(end_name) if end_name >= 10 else '0' + str(end_name))} СБ'

    return '.'.join(name_parts)


def get_coordinate_selected_routing(sw_assem, selected_routing: str) -> list[float]:
    comp_routing = sw_assem.GetComponentByName(selected_routing)
    return comp_routing.Transform2.ArrayData[9:12]


def insert_template_routing(selected_file: str, selected_routing: tuple[int, str]) -> None:
    with SolidWorksHandler() as sw:
        assem_dir: str = sw.model.GetPathName
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
            coord_routing: list[float] = get_coordinate_selected_routing(sw.model, selected_routing[2])

        arg1 = create_com(2, pythoncom.VT_BYREF | pythoncom.VT_I4)
        arg2 = create_com(128, pythoncom.VT_BYREF | pythoncom.VT_I4)
        doc_type: int = 2
        if new_name_template.lower().endswith('sldprt'):
            doc_type = 1
        for i in range(3):
            if sw.app.OpenDoc6(new_name_template, doc_type, 0, '', arg1, arg2):
                break
        sw.model.AddComponent5(new_name_template, 0, '', False, '', *coord_routing)
        sw.app.CloseDoc(new_name_template)
