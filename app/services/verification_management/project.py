from pathlib import Path

from services.sw_utils import get_sw_app_and_model, SwError, assembly_verification


def get_number_project(dir_project: str) -> str:
    return Path(dir_project).stem.split('.')[1]


def get_dir_project() -> tuple:
    try:
        sw_app, sw_assem = get_sw_app_and_model()
    except SwError as e:
        raise SwError(str(e))

    try:
        assembly_verification(sw_assem)
    except SwError as e:
        raise SwError(str(e))

    return sw_assem.GetPathName, sw_app, sw_assem
