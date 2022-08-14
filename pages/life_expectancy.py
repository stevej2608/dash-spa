from dash import html, dcc, dash_table, callback
from dash.exceptions import PreventUpdate
from dash_spa import register_page
import collections
import pandas as pd

from pages import LIFE_EXPECTANCY_SLUG

page = register_page(__name__, path=LIFE_EXPECTANCY_SLUG, title="Dash - Life Expectancy", short_name='Life Expectancy')

# Share Data Between Callbacks
# https://dash.plotly.com/dash-core-components/store


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

store =  dcc.Store(id=page.id('memory-output'))

countries_dropdown = dcc.Dropdown(df.country.unique(),
                 ['Canada', 'United States'],
                 id=page.id('countries_dropdown'),
                 multi=True)

life_dropdown = dcc.Dropdown({'lifeExp': 'Life expectancy', 'gdpPercap': 'GDP per capita'},
                 'lifeExp',
                 id=page.id('life_dropdown'))

graph = dcc.Graph(id='graph')

table = dash_table.DataTable(
            id=page.id('table'),
            columns=[{'name': i, 'id': i} for i in df.columns])


layout = html.Div([store, countries_dropdown, life_dropdown, html.Div([graph, table])])


@callback(store.output.data, countries_dropdown.input.value)
def filter_countries(countries_selected):
    if not countries_selected:
        # Return all the rows on initial load/no country selected.
        return df.to_dict('records')

    filtered = df.query('country in @countries_selected')

    return filtered.to_dict('records')


@callback(table.output.data,store.input.data)
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate

    return data

@callback(graph.output.figure, store.input.data, life_dropdown.input.value)
def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate

    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in data:

        a = aggregation[row['country']]

        a['name'] = row['country']
        a['mode'] = 'lines+markers'

        a['x'].append(row[field])
        a['y'].append(row['year'])

    return {
        'data': [x for x in aggregation.values()]
    }


