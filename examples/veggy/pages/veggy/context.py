from dash_spa.spa_context import  createContext, ContextState, dataclass

@dataclass
class TCartItem(ContextState):
    id: str = None
    count: int = 0
    price: float = 0.0
    name: str = ''
    image: str = ''


@dataclass
class TCartState(ContextState):
    isCartOpen: bool = False
    items: list = None
    search_term: str = ''

    def __post_init__(self):
        self.items = []
        super().__post_init__()

CartContext = createContext(TCartState)
