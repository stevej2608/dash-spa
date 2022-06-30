from typing import TypeVar, Union
import copy
from dash_spa.logging import log
from dataclasses import dataclass, field, _is_dataclass_instance, fields

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


# Modified version of /python3.8/dataclasses.py the dataclasses
# version in unable to handle missing fields

def asdict(obj, *, dict_factory=dict):
    """Return the fields of a dataclass instance as a new dictionary mapping
    field names to field values.

    Example usage:

      @dataclass
      class C:
          x: int
          y: int

      c = C(1, 2)
      assert asdict(c) == {'x': 1, 'y': 2}

    If given, 'dict_factory' will be used instead of built-in dict.
    The function applies recursively to field values that are
    dataclass instances. This will also look into built-in containers:
    tuples, lists, and dicts.
    """
    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):

            # Fix: Handle missing fields

            if hasattr(obj, f.name):
                value = _asdict_inner(getattr(obj, f.name), dict_factory)
                result.append((f.name, value))

        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        # obj is a namedtuple.  Recurse into it, but the returned
        # object is another namedtuple of the same type.  This is
        # similar to how other list- or tuple-derived classes are
        # treated (see below), but we just need to create them
        # differently because a namedtuple's __init__ needs to be
        # called differently (see bpo-34363).

        # I'm not using namedtuple's _asdict()
        # method, because:
        # - it does not recurse in to the namedtuple fields and
        #   convert them to dicts (using dict_factory).
        # - I don't actually want to return a dict here.  The main
        #   use case here is json.dumps, and it handles converting
        #   namedtuples to lists.  Admittedly we're losing some
        #   information here when we produce a json list instead of a
        #   dict.  Note that if we returned dicts here instead of
        #   namedtuples, we could no longer call asdict() on a data
        #   structure where a namedtuple was used as a dict key.

        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        # Assume we can create an object of this type by passing in a
        # generator (which is not true for namedtuples, handled
        # above).
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner(k, dict_factory),
                          _asdict_inner(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)

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
                if hasattr(self, '__shadow_update_listener__'):
                    self.__shadow_update_listener__()
            else:
                raise AttributeError(f"Attempt to write to undefined attribute {name}")

        super().__setattr__(name, value)

    def get_shadow_store(self):
        if not hasattr(self, '__shadow_store__'):
            self.set_shadow_store({})
        return self.__shadow_store__

    def set_shadow_store(self, store: dict, update_listener=None) -> None:
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
                    current_value.set_shadow_store(store[attr], update_listener)
                elif isinstance(current_value, list):
                    for idx, entry in enumerate(current_value):
                        if isinstance(entry, ContextState):
                            entry.set_shadow_store(store[attr][idx], update_listener)
                else:
                    setattr(self, attr, store[attr])

        # Update the new shadow dict with the current context

        for field in self.__dataclass_fields__:
            if not hasattr(self, field): continue
            current_value = getattr(self, field)
            if isinstance(current_value, ContextState):
                if not field in store:
                    store[field] = {}
                current_value.set_shadow_store(store[field], update_listener)
                #setattr(current_value, '__shadow_store__', store[field] )
            elif isinstance(current_value, list):
                if not field in store:
                    store[field] = [None for val in current_value]
                for idx, entry in enumerate(current_value):
                    if isinstance(entry, ContextState):
                        child_store = {}
                        entry.set_shadow_store(child_store, update_listener)
                        store[field][idx] = child_store
                        setattr(entry, '__shadow_store__', child_store)
            else:
                store[field] = current_value

        if update_listener:
            setattr(self, '__shadow_update_listener__', update_listener)

        setattr(self, '__shadow_store__', store)


    def update(self, ref: str = None, state: Union[SelfContextState, dict]= None) -> None:
        """ Copy the incoming state values to the context attributes """

        if ref is not None:
            if ref in self.__dataclass_fields__:
                value = getattr(self, ref)
                assert isinstance(value, ContextState), f"{ref} must be an instance of ContextState"
                value.update(state=state)
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

                if type(current_value) != type(new_value):
                    if isinstance(current_value, int):
                        new_value = int(new_value)
                    elif isinstance(current_value, float):
                        new_value = float(new_value)
                    else:
                        raise TypeError(f"Context update error, {attr}, unable to assign type {new_value}")

                setattr(self, attr, new_value)
