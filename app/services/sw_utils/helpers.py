import win32com.client


def create_com(value, *args):
    combined_flags = 0
    for flag in args:
        combined_flags |= flag

    return win32com.client.VARIANT(combined_flags, value)
