import pythoncom
import win32com.client

from .errors import SwAppError, SwModelError, SwAssemblyError


def get_sw_app_and_model():
    pythoncom.CoInitialize()
    sw_app = win32com.client.dynamic.Dispatch('SldWorks.Application')
    sw_model = sw_app.ActiveDoc

    if not sw_app:
        raise SwAppError()

    if not sw_model:
        raise SwModelError()

    return sw_app, sw_model


def assembly_verification(sw_model) -> None:
    if sw_model.GetType != 2:
        raise SwAssemblyError


def create_com(value, *args):
    if len(args) == 2:
        return win32com.client.VARIANT(args[0] | args[1], value)
    else:
        return win32com.client.VARIANT(args[0], value)
