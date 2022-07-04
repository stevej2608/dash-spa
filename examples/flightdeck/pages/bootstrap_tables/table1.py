from collections import OrderedDict
import pandas as pd
from dash import html
from dash_svg import Svg, Path
from dash_spa.components.table import TableContext
from .basic_table import BasicTable

EARTH_ICON =  Svg([
        Path(fillRule='evenodd', d='M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z', clipRule='evenodd')
    ], className='icon icon-xxs text-gray-500 me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

GOOGLE_ICON = Svg([
        Path(fill='currentColor', d='M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z')
    ], className='icon icon-xxs text-gray-500 me-2', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 488 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "google"})

YOUTUBE_ICON = Svg([
        Path(fill='currentColor', d='M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z')
    ], className='icon icon-xxs text-gray-500 me-2', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 576 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "youtube"})

YAHOO_ICON = Svg([
        Path(fill='currentColor', d='M223.69,141.06,167,284.23,111,141.06H14.93L120.76,390.19,82.19,480h94.17L317.27,141.06Zm105.4,135.79a58.22,58.22,0,1,0,58.22,58.22A58.22,58.22,0,0,0,329.09,276.85ZM394.65,32l-93,223.47H406.44L499.07,32Z')
    ], className='icon icon-xxs text-gray-500 me-2', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 512 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "yahoo"})

TWITTER_ICON = Svg([
        Path(fill='currentColor', d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z')
    ], className='icon icon-xxs text-gray-500 me-2', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 512 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "twitter"})

icons = {
    "Direct": EARTH_ICON,
    "Google Search": GOOGLE_ICON,
    "youtube.com": YOUTUBE_ICON,
    "yahoo.com": YAHOO_ICON,
    "twitter.com": TWITTER_ICON
}


data = OrderedDict([
    ('#',['1', '2', '3', '4', '5']),
    ('Traffic Source',['Direct', 'Google Search', 'youtube.com', 'yahoo.com', 'twitter.com']),
    ('Source Type',['Direct', 'Search/Organic', 'Social', 'Referral', 'Social']),
    ('Category',['-', '-', 'Arts and Entertainment', 'News and Media', 'Social Networks']),
    ('Global Rank',['--', '--', '#2', '#11', '#4']),
    ('Traffic Share',['51%', '18%', '18%', '8%', '4%']),
    ('Change',['2.45%', '17.78%', '-', '-9.45%', '-']),
    ])


df = pd.DataFrame.from_dict(data)

def progressBar(value):
    value = value[0:-1]
    return html.Td([
        html.Div([
            html.Div([
                html.Div(value, className='small fw-bold')
            ], className='col-12 col-xl-2 px-0'),
            html.Div([
                html.Div([
                    html.Div(className='progress-bar bg-dark',
                             role='progressbar',
                             style={"width": f"{value}%"}, **{"aria-valuenow": f"{value}", "aria-valuemin": "0", "aria-valuemax": "100"})
                ], className='progress progress-lg mb-0')
            ], className='col-12 col-xl-10 px-0 px-xl-1')
        ], className='row d-flex align-items-center')
    ])


class TrafficTable(BasicTable):

    def tableRow(self, index, args):

        cid, ts, st, cat, rank, share, change = args.values()

        return html.Tr([
            html.Td([
                html.A(cid, href='#', className='text-primary fw-bold')
            ]),
            html.Td([
                icons[ts],
                ts
            ], className='fw-bold d-flex align-items-center'),
            html.Td(st),
            html.Td(cat),
            html.Td(rank),
            progressBar(share),
            self.numberAndArrow(change)
        ])


def table1():

    table = TrafficTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns])


    return html.Div([
        html.Div([
            html.Div(table, className='table-responsive')
        ], className='card-body')
    ], className='card border-0 shadow mb-4')
