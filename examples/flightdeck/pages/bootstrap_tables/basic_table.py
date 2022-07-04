from abc import abstractmethod
from dash import html
from dash_svg import Svg, Path
from dash_spa.components.table import TableAIO

UP_ICON = Svg([
        Path(fillRule='evenodd', d='M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z', clipRule='evenodd')
    ], className='icon icon-xs me-1', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

DOWN_ICON = Svg([
        Path(fillRule='evenodd', d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z', clipRule='evenodd')
    ], className='icon icon-xs me-1', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')



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
            if v[0] =='-': return DOWN_ICON, v[1:], 'text-danger'
            return UP_ICON, v, 'text-success'

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