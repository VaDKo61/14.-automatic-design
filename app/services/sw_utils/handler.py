import pythoncom
import traceback

import win32com.client

from .errors import SwAppError, SwModelError, SwAssemblyError


class SolidWorksHandler:
    """Обёртка для безопасной работы с SolidWorks через COM."""

    def __init__(self):
        self.app = None
        self.model = None
        self._com_initialized = False

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()
        traceback.print_exception(exc_type, exc_val, exc_tb)  # Отладка
        return False

    def verify_assembly(self):
        if self.model.GetType != 2:
            raise SwAssemblyError

    def _connect(self):
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

    def _close(self):
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
