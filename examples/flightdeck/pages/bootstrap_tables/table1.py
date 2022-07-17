from collections import OrderedDict
import pandas as pd
from dash import html
from .basic_table import BasicTable
from ..icons import ICON, TWITTER, YOUTUBE, GOOGLE, YAHOO


icons = {
    "Direct": ICON.GLOBE,
    "Google Search": GOOGLE,
    "youtube.com": YOUTUBE.ME2,
    "yahoo.com": YAHOO,
    "twitter.com": TWITTER.ME2
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
