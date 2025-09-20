from services.sw_utils import get_sw_app_and_model
from .files import copy_template


def insert_template_routing(selected_file: str, selected_routing: tuple[int, str]):
    sw_app, sw_assem = get_sw_app_and_model()
    assem_dir: str = sw_assem.GetPathName
    begin_name_new_template: str = selected_routing[1][:-2]
    end_name: int = selected_routing[0] + 1
    end_name_new_template: str = str(end_name) if end_name >= 10 else '0' + str(end_name)
    try:
        copy_template(
            selected_file,
            '\\'.join(assem_dir.split('\\')[:-1]),
            begin_name_new_template + end_name_new_template + '.SLDASM'
        )
    except FileExistsError as e:
        raise FileExistsError(e)

# AddComponent5
# GetPathName
