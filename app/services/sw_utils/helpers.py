import pythoncom
import win32com.client


def create_com(value, *args):
    combined_flags = 0
    for flag in args:
        combined_flags |= flag

    return win32com.client.VARIANT(combined_flags, value)


def select_by_id(sw, name: str, type_obj: str) -> None:
    vt_dispatch = create_com(None, pythoncom.VT_DISPATCH)
    sw.model.Extension.SelectByID2(
        name,
        type_obj,
        0,
        0,
        0,
        False,
        0,
        vt_dispatch,
        0
    )
