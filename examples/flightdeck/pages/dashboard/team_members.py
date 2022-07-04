from dash import html, dcc

from ..icons.hero import CALENDER_ICON

def _contact_button(contact):
    return dcc.Link([
        CALENDER_ICON,
        contact
    ], href='#', className='btn btn-sm btn-secondary d-inline-flex align-items-center')

def _teamMember(name, picture, text, status, contact):
    return  html.Li([
        html.Div([
            html.Div([
                # Avatar
                dcc.Link([
                    html.Img(className='rounded', alt='Image placeholder', src=f'../../assets/img/team/{picture}.jpg')
                ], href='#', className='avatar')
            ], className='col-auto'),
            html.Div([
                html.H4([
                    dcc.Link(name, href='#')
                ], className='h6 mb-0'),
                html.Div([
                    html.Div(className=f'bg-{status} dot rounded-circle me-1'),
                    html.Small(text)
                ], className='d-flex align-items-center')
            ], className='col-auto ms--2'),
            html.Div([
                _contact_button(contact)
            ], className='col text-end')
        ], className='row align-items-center')
    ], className='list-group-item px-0')


def teamMembers():
    return html.Div([
        html.Div([
            html.Div([
                html.H2("Team members", className='fs-5 fw-bold mb-0'),
                dcc.Link("See all", href='#', className='btn btn-sm btn-primary')
            ], className='card-header border-bottom d-flex align-items-center justify-content-between'),
            html.Div([
                html.Ul([
                    _teamMember("Chris Wood","profile-picture-1","Online", "success", "Invite"),
                    _teamMember("Jose Leos","profile-picture-2","In a meeting", "warning", "Message"),
                    _teamMember("Bonnie Green","profile-picture-3","Offline", "danger", "Message"),
                    _teamMember("Neil Sims","profile-picture-4","Offline", "danger", "Message"),
                ], className='list-group list-group-flush list my--3')
            ], className='card-body')
        ], className='card border-0 shadow')
    ], className='col-12 col-xxl-6 mb-4')
