from abc import abstractmethod
from dash import html
from dash_svg import Svg, Path
from dash_spa.components.table import TableAIO
from ..icons import ICON


class BasicTable(TableAIO):

    TABLE_CLASS_NAME = 'table table-centered table-nowrap mb-0 rounded'

    def tableHead(self, columns):

        names = [col['name'] for col in columns]

        beg = html.Th(names[0], className='border-0 rounded-start')
        mid = [html.Th(name, className='border-gray-200') for name in names[1:-1]]
        end = html.Th(names[-1], className='border-0 rounded-end')

        row = html.Tr([beg] + mid +[end])

        return html.Thead(row, className='thead-light')


    def numberAndArrow(self, value):

        def normalise(v):
            if v == '-': return None, v, None
            if v[0] =='-': return ICON.DOWN_ARROW.ME1, v[1:], 'text-danger'
            return ICON.UP_ARROW.ME1, v, 'text-success'

        icon, text, text_colour = normalise(value)

        return html.Td([
            html.Div([
                icon,
                html.Span(text, className='fw-bold')
            ], className='d-flex align-items-center')
        ], className=text_colour)

    @abstractmethod
    def tableRow(self, args):
        return None