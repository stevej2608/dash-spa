from dash_spa.logging import log
from dash import html, dcc
from dash_spa import prefix
from pandas import DataFrame

from .icons import SEARCH
from .context import TableContext

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
                        if value_part.lower() == 'true':
                            value = True
                        elif value_part.lower() == 'false':
                            value = False
                        else:
                            value = float(value_part)
                    except ValueError:
                        value = value_part
                # word _operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def filter_dash(df: DataFrame, filter_query: str) -> DataFrame:
    """Filter a Pandas dataframe as per the `filter_query` provided by
    the DataTable.

    ```
    filter_query is of the form:

        {salary} gt 30000 && {city} eq {london} && {age} eq  35
    ```

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


def filter_str_generic(df: DataFrame, value: str) -> DataFrame:

    col_names = list(df.columns)

    def filter_fn(row):
        for col in col_names:
            if str(row[col]) == value:
                return True

        return False

    m = df.apply(filter_fn, axis=1)

    df1 = df[m]
    return df1


# https://stackoverflow.com/a/43018248/489239

def filter_str(df: DataFrame, value: str, case=False) -> DataFrame:
    """Return df rows that contain given is any of the rows cells string

    Args:
        df (DataFrame): Data frame to be filtered
        value (str): String the must be contained in row
        case (bool, optional): True is test is case sensitive. Defaults to False.

    Returns:
        _type_: _description_
    """

    if value:
        return  df[df.apply(lambda row: row.astype(str).str.contains(value, case=case).any(), axis=1)]
    else:
        return df


class SearchAIO(html.Div):

    def __init__(self, id, placeholder='Search...', minimum_characters=0):

        search_term, setSearchTerm = TableContext.useState('search_term')

        pid = prefix(id)

        # log.info('search init term=[%s]', search_term)

        # The search input has an associated one-shot retriggerable timer that
        # is re-armed each time the user enters a character. Only when the timer
        # expires is the search term updated.

        search = dcc.Input(id=pid('search'), className='form-control', type="text", value=search_term, placeholder=placeholder)
        delay = dcc.Interval(id=pid('delay'), max_intervals=1, interval=1200, disabled=True)

        # User input arms/rearms the timer

        @TableContext.callback(delay.output.disabled, delay.output.interval, search.input.value, delay.state.interval, prevent_initial_call=True)
        def delay_cb(value, interval, state):

            # This is the only way I've found to get the timer to rearm

            return False, interval+1

        # Timer has expired update the search term

        @TableContext.On(delay.input.n_intervals, search.state.value, prevent_initial_call=True)
        def search_cb(interval, value):
            setSearchTerm(value)

        ui = html.Div([
            html.Span(SEARCH, className='input-group-text'),
            search,
            delay
        ], className='input-group me-2 me-lg-3 fmxw-400')

        super().__init__(ui, className='col col-md-6 col-lg-3 col-xl-4')
