from dash import html
from dash_spa import register_page

from .common import breadCrumbs, banner, topNavBar, footer
from .bootstrap_tables import table1, table2


register_page(__name__, path="/pages/tables/bootstrap-tables", title="Dash/Flightdeck - Bootstrap Tables")

layout = html.Main([
        topNavBar(),
        html.Div([
            breadCrumbs(["Tables","Bootstrap tables"]),
            banner("Bootstrap tables", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/tables/')
        ], className='py-4'),
        table1(),
        table2(),
        footer()
    ], className='content')

