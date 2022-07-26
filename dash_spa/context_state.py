from typing import TypeVar, Union
from dataclasses import dataclass, field
from dash_spa.logging import log

from .utils.dataclass import asdict

# ContextState is a base class
#
# Used by:
#
#  dash_spa/spa_context.py React.js style context pattern
#  dash_spa/plugins/spa_session.py

# https://docs.python.org/3/library/dataclasses.html

SelfContextState = TypeVar("SelfContextState", bound="ContextState")


EMPTY_LIST = field(default_factory=lambda: [])
EMPTY_DICT = field(default_factory=lambda: {})

@dataclass(init=False)
class ContextState:
    """ ContextState is a simple wrapper to enable dot
    autocompletion to the underlying dictionary

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

    def __post_init__(self):
        self.__strict__ = True

    def cid(self):
        """Unique context ID"""
        return id(self)


    def __setattr__(self, name, value):

        if hasattr(self, '__strict__') and not name.startswith('__'):
            if name in self.__dataclass_fields__ or not self.__strict__:
                super().__setattr__(name, value)
                if hasattr(self, '__shadow_update_listener__'):
                    self.__shadow_update_listener__(self.asdict())
            else:
                raise AttributeError(f"Attempt to write to undefined attribute {name}")
        else:
            super().__setattr__(name, value)


    def asdict(self):
        return asdict(self)

    def update(self, ref: str = None, state: Union[SelfContextState, dict] = None, update_listener=None) -> None:
        """ Copy the incoming state values to the context attributes """

        if update_listener:
            setattr(self, '__shadow_update_listener__', update_listener)

        if ref is not None:

            if ref in self.__dataclass_fields__:
                value = getattr(self, ref)
                assert isinstance(value, ContextState), f"{ref} must be an instance of ContextState"
                value.update(state=state)
                return

            if not self.__strict__:
                if not hasattr(self, ref):
                    setattr(self, ref, state)
                    self.__dataclass_fields__[ref] = field()
                    return

            raise AttributeError(f"Unknown attribute {ref}")

        # Iterate over incoming fields...

        if isinstance(state, ContextState):
            state = asdict(state)

        for attr in self.__dataclass_fields__:

            if not attr in state:
                continue

            new_value = state[attr]

            # If the attr is a ContextState do some checks and
            # call ourselves recursively

            current_value = getattr(self, attr)

            if isinstance(current_value, ContextState):
                current_value.update(state=new_value)

            else:
                try:

                    # Convert dict strings to numeric types

                    if type(current_value) != type(new_value):
                        if isinstance(current_value, int):
                            new_value = int(new_value)
                        elif isinstance(current_value, float):
                            new_value = float(new_value)

                    setattr(self, attr, new_value)

                except Exception:
                    raise TypeError(f"Context update error, {attr}, unable to assign type {new_value}")
