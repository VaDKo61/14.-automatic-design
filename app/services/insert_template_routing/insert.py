import pythoncom

from pathlib import Path

from .files import _copy_template
from ..sw_utils.handler import SolidWorksHandler
from ..sw_utils.helpers import create_com


def insert_template_routing(
        selected_file: str,
        selected_routing: tuple[int, str, str]
) -> None:
    with SolidWorksHandler() as sw:
        assem_dir: Path = Path(sw.model.GetPathName)
        target_dir: Path = assem_dir.parent

        new_name_template: str = _create_new_name(selected_routing, selected_file)

        try:
            _copy_template(selected_file, str(target_dir), new_name_template)
        except FileExistsError:
            raise FileExistsError(f'Файл {new_name_template} уже существует')

        if selected_routing[0] == -1:
            coord_routing: list[float] = [0.0, 0.1, 0.0]
        else:
            coord_routing: list[float] = _get_coordinate_selected_routing(
                sw.model,
                selected_routing[2]
            )

        arg1 = create_com(2, pythoncom.VT_BYREF | pythoncom.VT_I4)
        arg2 = create_com(128, pythoncom.VT_BYREF | pythoncom.VT_I4)
        doc_type = 1 if new_name_template.lower().endswith('sldprt') else 2

        for i in range(3):
            if sw.app.OpenDoc6(new_name_template, doc_type, 0, '', arg1, arg2):
                break
        else:
            raise Exception(f'Не удалось открыть документ: {new_name_template}')

        sw.model.AddComponent5(new_name_template, 0, '', False, '', *coord_routing)
        sw.app.CloseDoc(new_name_template)


def _create_new_name(selected_routing: tuple[int, str, str], selected_file: str) -> str:
    index, routing_name, _ = selected_routing
    suffix: str = Path(selected_file).suffix

    if index == -1:
        return routing_name + suffix

    name_parts: list[str] = routing_name.split('.')
    end_name: int = index + 1
    name_parts[-2] = f'{end_name:02d} СБ'

    return '.'.join(name_parts)


def _get_coordinate_selected_routing(sw_assem, selected_routing: str) -> list[float]:
    comp_routing = sw_assem.GetComponentByName(selected_routing)
    if not comp_routing:
        raise ValueError(f"Компонент '{selected_routing}' не найден в сборке.")

    coordinate: list[float] = list(comp_routing.Transform2.ArrayData[9:12])
    coordinate[1] += 0.1

    return coordinate
