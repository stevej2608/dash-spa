from dash_spa.components.StoreState import StoreState

class PaginationState(StoreState):
    """Paginator status

    Properties:
        page (int): Current page value
        page_size (int): Page size
        last_page (int): The last page
    """
    @property
    def page(self):
        return self.data['page']

    @property
    def page_size(self):
        return self.data['page_size']

    @property
    def last_page(self):
        return self.data['last_page']
