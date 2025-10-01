from services.sw_utils import SwError
from .project import get_dir_project, get_number_project
from .sp import get_dir_sp, save_sp_assem, save_verification_excel


def verification_sp():
    try:
        dir_project, sw_app, sw_assem = get_dir_project()
    except SwError as e:
        raise SwError(str(e))

    number_project: str = get_number_project(dir_project)
    try:
        dir_sp: str = get_dir_sp(dir_project, number_project)
    except FileNotFoundError as e:
        raise FileNotFoundError(e)

    try:
        dir_sp_assem: str = save_sp_assem(sw_assem, dir_sp, number_project)
    except SwError as e:
        raise SwError

    save_verification_excel(dir_sp, dir_sp_assem)