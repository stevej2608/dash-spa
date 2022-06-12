from typing import TypeVar
from dataclasses import dataclass
from dash_spa.logging import log


# https://docs.python.org/3/library/dataclasses.html


SelfContextState = TypeVar("SelfContextState", bound="ContextState")

@dataclass
class ContextState:
    """ ContextState is a simple wrapper to enable dot
    autocompletion to the underlying dcc.Store data dictionary

    Usage:
    ```
        @dataclass
        class TableState(ContextState):
            current_page: int = 1
            page_size: int = 10
            last_page: int = 1
            table_rows: int = 0
            search_term: str = None

        state = TableState()
        state.map_store(store)

    ```
    """

    @property
    def state(self):
        if hasattr(self, '_state'):
            return self._state
        else:
            state = self.__dict__.copy()
            state.pop('__store_keys__', None)
            return state


    def __setattr__(self, name, value):

        if hasattr(self, '_state') and name != '_state':
            if name in self.__store_keys__:
                self._state[name] = value
            else:
                raise AttributeError(f"Attempt to write to undefined attribute {name}")

        elif name not in ['__store_keys__', '_state']:
            if not hasattr(self, '__store_keys__'):
                self.__store_keys__ = []
            if name not in self.__store_keys__:
                self.__store_keys__.append(name)

        super().__setattr__(name, value)


    def map_store(self, store: dict) -> None:
        """Map the incoming dict onto the ContextState. When
        context attributes are changed the store value will be updated

        Args:
            store (dict): The latest dcc.Store state
        """

        # Copy the incoming store values to the context attributes

        for attr in store.keys():
            if attr in self.__store_keys__:
                value = getattr(self, attr)
                if isinstance(value, ContextState):
                    value.map_store(store[attr])
                else:
                    setattr(self, attr, store[attr])

        # Update the new shadow dict with the current context

        for attr in self.__store_keys__:
            value = getattr(self, attr)
            if isinstance(value, ContextState):
                child_store = store[attr] if attr in store else {}
                value.map_store(child_store)
                store[attr] = child_store
            else:
                store[attr] = value


        self._state = store


    def update(self, ref: str = None, state: SelfContextState = None) -> None:
        """ Copy the incoming state values to the context attributes """

        if ref is not None:
            if ref in self.__store_keys__:
                value = getattr(self, ref)
                if isinstance(value, ContextState):
                    value.update(state=state)
                else:
                    setattr(self, ref, state)
                return

            raise AttributeError(f"Unknown attribute {ref}")

        for attr in self.__store_keys__:
            if hasattr(state, attr):
                value = getattr(state, attr)
                if value is not None:
                    setattr(self, attr, value)
            else:
                raise AttributeError(f"Unknown attribute {ref}")

