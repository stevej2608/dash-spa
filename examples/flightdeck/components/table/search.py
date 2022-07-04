from holoniq.utils import log
from dash import html, dcc, callback
from dash_spa import prefix
from components.store_aio import StoreAIO
from icons.hero import SEARCH_ICON

# https://dash.plotly.com/datatable/callbacks#backend-paging-with-filtering

_operators = [
    ['ge ', '>='],
    ['le ', '<='],
    ['lt ', '<'],
    ['gt ', '>'],
    ['ne ', '!='],
    ['eq ', '='],
    ['contains '],
    ['datestartswith ']]

def _split_filter_part(filter_part):
    for operator_type in _operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                # word _operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def filter_df(df, filter_query):
    """Filter a Pandas dataframe as per the `filter_query` provided by
    the DataTable.
    """

    try:

        filtering_expressions = filter_query.split(' && ')
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = _split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these _operators match pandas series operator method names
                df = df.loc[getattr(df[col_name], operator)(filter_value)]
            elif operator == 'contains':
                df = df.loc[df[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                df = df.loc[df[col_name].str.startswith(filter_value)]

    except:
        pass

    return df


class SearchAIO(html.Div):

    def __init__(self, placeholder='Search...',  aio_id=None):

        self.store = StoreAIO.create_store({'search': ''}, aio_id)
        pid = prefix(self.store.id)

        search = dcc.Input(id=pid('input'), type='text', className='form-control', placeholder=placeholder)

        @callback(self.store.output.data, search.input.value, self.store.state.data)
        def _cb(value, store):
            log.info('value = [%s]', value)
            store['search'] = value
            return store


        ui = html.Div([
            html.Span(SEARCH_ICON, className='input-group-text'),
            search
        ], className='input-group me-2 me-lg-3 fmxw-400')

        super().__init__(ui, className='col col-md-6 col-lg-3 col-xl-4')
