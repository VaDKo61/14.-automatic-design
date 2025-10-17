import pythoncom
import win32com.client

from .errors import SwAppError, SwModelError, SwAssemblyError


class SolidWorksHandler:
    """Обёртка для безопасной работы с SolidWorks через COM."""

    def __init__(self):
        self.app = None
        self.model = None
        self._com_initialized = False

    def connect(self):
        if not self._com_initialized:
            pythoncom.CoInitialize()
            self._com_initialized = True

        try:
            self.app = win32com.client.Dispatch('SldWorks.Application')
            self.model = self.app.ActiveDoc
        except Exception as e:
            raise SwAppError(f'Ошибка подключения к SolidWorks: {e}')

        if not self.app:
            raise SwAppError()
        if not self.model:
            raise SwModelError()

        self._enable_boost(False)

    def close(self):
        self._enable_boost(True)

        try:
            self.model = None
            self.app = None
        finally:
            if self._com_initialized:
                pythoncom.CoUninitialize()
                self._com_initialized = False

    def _enable_boost(self, enable: bool):
        self.model.UnLock() if enable else self.model.Lock()
        self.model.FeatureManager.EnableFeatureTree = enable
        self.model.FeatureManager.EnableFeatureTreeWindow = enable
        self.model.ConfigurationManager.EnableConfigurationTree = enable
        self.model.ActiveView.EnableGraphicsUpdate = enable

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


def get_sw_app_and_model():
    pythoncom.CoInitialize()
    sw_app = win32com.client.dynamic.Dispatch('SldWorks.Application')
    sw_model = sw_app.ActiveDoc

    if not sw_app:
        raise SwAppError()

    if not sw_model:
        raise SwModelError()

    return sw_app, sw_model


def verification_assembly(sw_model) -> None:
    if sw_model.GetType != 2:
        raise SwAssemblyError


def create_com(value, *args):
    combined_flags = 0
    for flag in args:
        combined_flags |= flag

    return win32com.client.VARIANT(combined_flags, value)
