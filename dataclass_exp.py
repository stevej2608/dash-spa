import json
from dataclasses import _process_class, field

def _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id):
    setattr(cls, '__session_id__', id)
    cls = _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)
    return cls


def session_data(cls=None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, id=None):

    def wrap(cls):
        return _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id)

    # See if we're being called as @dataclass or @dataclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dataclass without parens.
    return wrap(cls)


class ContextState:
    name = 'ContextState'

    def __init__(self):
        super().__init__()
        print(self.__dict__)
        pass

    def __str__(self):
        return f"{self.__session_id__}:{json.dumps(self.__dict__)}"


# https://www.uuidgenerator.net/version4

@session_data(id="c8f67e4e")
class TestState(ContextState):
    id = 99
    current_page: int = 1
    page_size: int = 10
    last_page: int = 1
    table_rows: int = 0
    search_term: str = None
    sizes: list = field(default_factory=lambda: [10, 20, 30])


if __name__ == "__main__":

    test1 = TestState()
    test2 = TestState()

    test1.id = 66
    test1.sizes[0] = 99
    test2.id = 33

    print(test1)
    print(test2)

