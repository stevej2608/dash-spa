from typing import TypeVar
from dash_spa.logging import log
from dataclasses import dataclass, field, asdict, _is_dataclass_instance

# ContextState is a simple wrapper enabling dot notation
# the underlying dictionary.
#
# Used by:
#
#  dash_spa/spa_context.py React.js style context pattern
#  dash_spa/plugins/spa_session.py

# https://docs.python.org/3/library/dataclasses.html

SelfContextState = TypeVar("SelfContextState", bound="ContextState")


EMPTY_LIST = field(default_factory=lambda: [])
EMPTY_DICT = field(default_factory=lambda: {})

# @dataclass
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

    @property
    def cid(self):
        return id(self)

    def __init__(self):
        self.__shadow_store__ = {}


    def __setattr__(self, name, value):

        if hasattr(self, '__shadow_store__') and name != '__shadow_store__':
            if name in self.__dataclass_fields__:
                self.__shadow_store__[name] = value
            else:
                raise AttributeError(f"Attempt to write to undefined attribute {name}")

        super().__setattr__(name, value)

    def get_shadow_store(self):
        if not hasattr(self, '__shadow_store__'):
            self.set_shadow_store({})
        return self.__shadow_store__

    def set_shadow_store(self, store: dict) -> None:
        """Use the given dict as the context shadow store.

        The mapping proceeds as follows: The context structure is traversed
        and elements in the store, if present, are used to update the
        corresponding context attribute. The context structure
        is then traversed a again, this time context attributes use used
        to update the store.

        The given store is used as the new shadow store. Changes in
        context attributes automatically update the corresponding
        shadow store entry.

        Args:
            store (dict): The shadow store state
        """

        # Copy the incoming shadow dict values to the the current context

        for attr in store.keys():
            if attr in self.__dataclass_fields__:
                current_value = getattr(self, attr)
                if isinstance(current_value, ContextState):
                    current_value.set_shadow_store(store[attr])
                elif isinstance(current_value, list):
                    for idx, entry in enumerate(current_value):
                        if isinstance(entry, ContextState):
                            entry.set_shadow_store(store[attr][idx])
                else:
                    setattr(self, attr, store[attr])

        # Update the new shadow dict with the current context

        for field in self.__dataclass_fields__:
            if not hasattr(self, field): continue
            current_value = getattr(self, field)
            if isinstance(current_value, ContextState):
                if not field in store:
                    store[field] = {}
                current_value.set_shadow_store(store[field])
                #setattr(current_value, '__shadow_store__', store[field] )
            elif isinstance(current_value, list):
                if not field in store:
                    store[field] = [None for val in current_value]
                for idx, entry in enumerate(current_value):
                    if isinstance(entry, ContextState):
                        child_store = {}
                        entry.set_shadow_store(child_store)
                        store[field][idx] = child_store
                        setattr(entry, '__shadow_store__', child_store)
            else:
                store[field] = current_value

        setattr(self, '__shadow_store__', store)


    def update(self, ref: str = None, state: SelfContextState = None) -> None:
        """ Copy the incoming state values to the context attributes """

        if ref is not None:
            if ref in self.__dataclass_fields__:
                value = getattr(self, ref)
                assert isinstance(value, ContextState), f"{ref} must be an instance of ContextState"
                value.update(state=state)
                return

            raise AttributeError(f"Unknown attribute {ref}")

        # Iterate over incoming fields...

        for attr in state.__dataclass_fields__:

            if not hasattr(state, attr):
                continue

            # Confirm we have this field

            assert attr in self.__dataclass_fields__, f"Attempt to update none unknown field self.{attr}"

            # Get the incoming field value

            new_value = getattr(state, attr)

            # If the incoming value is a ContextState do some checks and
            # call ourselves recursively

            if isinstance(new_value, ContextState):
                current_value = getattr(self, attr)
                assert isinstance(current_value, ContextState), f"self.{attr} and must be an instance of ContextState"
                current_value.update(state=new_value)

            else:
                setattr(self, attr, new_value)

