from dash import html
from dash_spa import register_page, prefix, SPA_LOCATION, url_for, NOUPDATE
from dash_spa.components.table import TableAIOPaginator, TableAIOPaginatorView, TableContext

from .common import breadCrumbs, topNavBar, footer
from .transactions import create_table, create_header
from .icons import ICON


page = register_page(__name__, path="/pages/transactions", title="Dash/Flightdeck - Transactions")


def button(text):
    return html.Button(text, type='button', className='btn btn-sm btn-outline-gray-600')

def newPlanButton():
    return html.A([ICON.PLUS, "New Plan"], href='#', className='btn btn-sm btn-gray-800 d-inline-flex align-items-center')


@TableContext.Provider(id='transactions_table')
def layout_transactions_table(**_kwargs):

    pid = prefix('transactions_table')

    state = TableContext.getState(update=_kwargs)

    # log.info('layout_transactions_table: %s', state)

    # Create the table components

    table = create_table(id=pid())
    header = create_header(id=pid('header'))
    paginator = TableAIOPaginator(className='pagination mb-0', id=pid('paginator'))
    viewer = TableAIOPaginatorView()

    # Update the browser address bar whenever the table state changes

    @SPA_LOCATION.update(TableContext.store.input.data)
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

    # log.info('********** layout transactions.page %s ****************', kwargs)

    transactions_table = layout_transactions_table(**kwargs)

    return html.Main([
            topNavBar(),
            html.Div([
                html.Div([
                    breadCrumbs(["Volt", "Transactions"]),
                    html.H2("All Orders", className='h4'),
                    html.P("Your web analytics dashboard template.", className='mb-0')
                ], className='d-block mb-4 mb-md-0'),
                html.Div([
                    newPlanButton(),
                    html.Div([
                        button("Share"),
                        button("Export")
                    ], className='btn-group ms-2 ms-lg-3')
                ], className='btn-toolbar mb-2 mb-md-0')

            ], className='d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4'),
            transactions_table,
            footer()
        ], className='content')
