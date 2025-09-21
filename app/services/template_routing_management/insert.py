import pythoncom

from services.sw_utils import get_sw_app_and_model, create_com
from .files import copy_template


def create_new_name(selected_routing: tuple[int, str]) -> str:
    if selected_routing[0] == -1:
        return selected_routing[1] + '.SLDASM'
    begin_name_new_template: str = selected_routing[1].split('-')[0][:-2]
    end_name: int = selected_routing[0] + 1
    end_name_new_template: str = str(end_name) if end_name >= 10 else '0' + str(end_name)
    return begin_name_new_template + end_name_new_template + '.SLDASM'


def get_coordinate_selected_routing(sw_assem, selected_routing: str) -> list[float]:
    comp_routing = sw_assem.GetComponentByName(selected_routing)
    return comp_routing.Transform2.ArrayData[9:12]


def insert_template_routing(selected_file: str, selected_routing: tuple[int, str]) -> None:
    sw_app, sw_assem = get_sw_app_and_model()

    assem_dir: str = sw_assem.GetPathName
    new_name_template: str = create_new_name(selected_routing)

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
        coord_routing: list[float] = get_coordinate_selected_routing(sw_assem, selected_routing[1])

    arg1 = create_com(2, pythoncom.VT_BYREF | pythoncom.VT_I4)
    arg2 = create_com(128, pythoncom.VT_BYREF | pythoncom.VT_I4)
    sw_app.OpenDoc6(new_name_template, 2, 0, '', arg1, arg2)
    sw_assem.AddComponent5(new_name_template, 0, '', False, '', *coord_routing)
    sw_app.CloseDoc(new_name_template)
