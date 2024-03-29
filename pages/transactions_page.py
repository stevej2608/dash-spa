from dash import html

from dash_spa import register_page, prefix, url_for, NOUPDATE
from dash_spa.components import SPA_LOCATION, TableAIOPaginator, TableAIOPaginatorView, TableContext
from dash_spa.logging import log

from pages import TRANSACTIONS_SLUG
from .transactions import create_table, create_header
from .transactions.icons import ICON


page = register_page(__name__, path=TRANSACTIONS_SLUG, title="Dash/Flightdeck - Transactions", short_name='Transactions')

def button(text):
    return html.Button(text, type='button', className='btn btn-sm btn-outline-gray-600')

def newPlanButton():
    return html.A([ICON.PLUS, "New Plan"], href='#', className='btn btn-sm btn-gray-800 d-inline-flex align-items-center')


@TableContext.Provider()
def layout_transactions_table(query_string: dict = None):

    pid = prefix('transactions_table')

    state = TableContext.getState(update=query_string)

    log.info('layout_transactions_table: %s', state)

    # Create the table components

    table = create_table(id=pid())
    header = create_header(id=pid('header'))
    paginator = TableAIOPaginator(className='pagination mb-0', id=pid('paginator'))
    viewer = TableAIOPaginatorView()

    # Update the browser address bar whenever the table state changes

    @SPA_LOCATION.update(TableContext.store.input.data, prevent_initial_call=True)
    def update_location(state, location):
        if state:
            try:
                href = url_for(page.module, state, attr=['current_page', 'search_term'])
                return { 'href': href }
            except Exception:
                pass

        return NOUPDATE

    return html.Div([
        header,
        html.Div(table, className='card card-body border-0 shadow table-wrapper table-responsive'),
        html.Div([
            paginator,
            viewer
        ], className='card-footer px-3 border-0 d-flex flex-column flex-lg-row align-items-center justify-content-between')
    ])


def layout(**kwargs):

    log.info('********** layout transactions.page %s ****************', kwargs)

    transactions_table = layout_transactions_table(query_string=kwargs)

    return transactions_table
