import dash
from dash import _pages, _callback
from .logging import log


class GlobalContext:

    def __init__(self):
        log.info('Create GlobalContext')

        self.callback_index = 0

        self._saved=False

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


    def save(self):

        if not self._saved:
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

            self._saved = True


    def restore(self):

        def list_merge(first_list, second_list):

            for entry in second_list:
                if not entry in first_list:
                    first_list.append(entry)

        if self._saved:

            log.info('GlobalContext: - restore')

            # self.PAGE_REGISTRY.update(self._PAGE_REGISTRY)

            list_merge(self.GLOBAL_CALLBACK_LIST, self._GLOBAL_CALLBACK_LIST)
            self.GLOBAL_CALLBACK_MAP.update(self._GLOBAL_CALLBACK_MAP)

            # self._page_container = self.page_container.copy()
            # self._location = self.location.copy()

            self.container_registry.update(self._container_registry)
            list_merge(self.style_registry, self._style_registry)

            list_merge(self.external_scripts, self._external_scripts)
            list_merge(self.external_stylesheets, self._external_stylesheets)
            list_merge(self.internal_stylesheets, self._internal_stylesheets)

    def clear(self):
        self.callback_index = 0
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

        while len(self.page_container.children) > 4:
            self.page_container.children.pop()


    def dump(self):
        log.info('**************** dump() ************************')
        index = 0
        for id in self.GLOBAL_CALLBACK_MAP.keys():
            if index >= self.callback_index:
                log.info('%d %s', index, id)
            index +=1
        self.callback_index = index

        index = 0
        for page in self.PAGE_REGISTRY.values():
            log.info('%d %s', index, page['module'])
            index +=1

        log.info('************************************************')


Globals = GlobalContext()
