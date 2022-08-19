import dash
from dash import _pages, _callback
from .logging import log


class GlobalContext:


    def __init__(self):
        log.info('Create GlobalContext')

        self.save=True
        self.restore=False

        self.PAGE_REGISTRY = _pages.PAGE_REGISTRY

        self.GLOBAL_CALLBACK_LIST = _callback.GLOBAL_CALLBACK_LIST
        self.GLOBAL_CALLBACK_MAP = _callback.GLOBAL_CALLBACK_MAP

        self.page_container = dash.page_container
        self.location = self.page_container.children[0]

        self.container_registry = {}
        self.style_registry = []

        self.external_scripts = []
        self.external_stylesheets = []
        self.internal_stylesheets = []


    def save_or_restore(self):

        def list_merge(first_list, second_list):

            for entry in second_list:
                if not entry in first_list:
                    first_list.append(entry)


        if self.save:
            log.info('GlobalContext: - save')
            self._PAGE_REGISTRY = self.PAGE_REGISTRY.copy()

            self._GLOBAL_CALLBACK_LIST = self.GLOBAL_CALLBACK_LIST.copy()
            self._GLOBAL_CALLBACK_MAP = self.GLOBAL_CALLBACK_MAP.copy()

            # self._page_container = self.page_container.copy()
            # self._location = self.location.copy()

            self._container_registry = self.container_registry.copy()
            self._style_registry = self.style_registry.copy()

            self._external_scripts = self.external_scripts.copy()
            self._external_stylesheets = self.external_stylesheets.copy()
            self._internal_stylesheets = self.internal_stylesheets.copy()

            self.save = False
            self.restore = True

            return

        if self.restore:

            log.info('GlobalContext: - restore')

            self.PAGE_REGISTRY.update(self._PAGE_REGISTRY)

            list_merge(self.GLOBAL_CALLBACK_LIST, self._GLOBAL_CALLBACK_LIST)
            self.GLOBAL_CALLBACK_MAP.update(self._GLOBAL_CALLBACK_MAP)

            self._page_container = self.page_container.copy()
            self._location = self.location.copy()

            list_merge(self.container_registry, self._container_registry)
            list_merge(self.style_registry, self._style_registry)

            list_merge(self.external_scripts, self._external_scripts)
            list_merge(self.external_stylesheets, self._external_stylesheets)
            list_merge(self.internal_stylesheets, self._internal_stylesheets)

            self.restore = False



    def clear(self):
        self.PAGE_REGISTRY.clear()

        self.GLOBAL_CALLBACK_LIST.clear()
        self.GLOBAL_CALLBACK_MAP.clear()

        # self._page_container = self.page_container.clear()
        # self._location = self.location.clear()

        self.container_registry.clear()
        self.style_registry.clear()

        self.external_scripts.clear()
        self.external_stylesheets.clear()
        self.internal_stylesheets.clear()







Globals = GlobalContext()
