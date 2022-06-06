from dash import html
from .context import TableContext

class TableAIOPaginatorView(html.Div):
    """Manages and updates the view component of the associated
    TableAIOPaginator. The TableAIOPaginatorView callback is triggered when the
    store component value changes. The callback calls the supplied
    'content' function. The function return value is rendered as the child
    element of the TableAIOPaginatorView

    Args:
        paginator (TableAIOPaginator): The associated paginator
        className (str): the className of the component

    Returns:
        html.Div: The view component

    Example:
    ```

        paginator = TableAIOPaginator(["Previous", 1, 2, 3, 4, 5, "Next"], 5, 25)
        viewer = TableAIOPaginatorView(paginator, render_content, className='fw-normal small mt-4 mt-lg-0' )
    ```

    Markup:
    ```
        <div class="fw-normal small mt-4 mt-lg-0">
            Showing page <b>4</b> out of <b>25</b> pages
        </div>
    ```
    """
    def __init__(self, className='fw-normal small mt-4 mt-lg-0'):
        state = TableContext.getState()
        content = ["Showing page ",html.B(state.current_page)," out of ",html.B(state.last_page)," pages"]
        super().__init__(content, className=className)
