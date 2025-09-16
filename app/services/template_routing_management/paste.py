from services.sw_utils import get_sw_app_and_model, SwError, assembly_verification
from .files import get_list_files


def paste_template_routing():
    try:
        sw_app, sw_model = get_sw_app_and_model()
    except SwError as e:
        raise SwError(str(e))

    try:
        assembly_verification(sw_model)
    except SwError as e:
        raise SwError(str(e))

    files: list = get_list_files()


# paste_template_routing()
