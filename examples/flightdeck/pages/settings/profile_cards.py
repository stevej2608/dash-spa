from dash import html, dcc

from ..common import background_img
from ..icons.hero import PAPER_CLIP, USER_ADD_BTN


def userPhotoCard():
    return html.Div([
        html.Div([
            html.Div(className='profile-cover rounded-top', style=background_img("/assets/img/profile-cover.jpg")),
            html.Div([
                html.Img(src='../assets/img/team/profile-picture-1.jpg', className='avatar-xl rounded-circle mx-auto mt-n7 mb-4', alt='Neil Portrait'),
                html.H4("Neil Sims", className='h3'),
                html.H5("Senior Software Engineer", className='fw-normal'),
                html.P("New York, USA", className='text-gray mb-4'),
                dcc.Link([
                    USER_ADD_BTN,
                    "Connect"
                ], className='btn btn-sm btn-gray-800 d-inline-flex align-items-center me-2', href='#'),
                dcc.Link("Send Message", className='btn btn-sm btn-secondary', href='#')
            ], className='card-body pb-5')
        ], className='card shadow border-0 text-center p-0')
    ], className='col-12 mb-4')

def profilePhotoCard():
    return html.Div([
        html.Div([
            html.H2("Select profile photo", className='h5 mb-4'),
            html.Div([
                html.Div([
                    # Avatar
                    html.Img(className='rounded avatar-xl', src='../assets/img/team/profile-picture-3.jpg', alt='change avatar')
                ], className='me-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            PAPER_CLIP,
                            dcc.Input(type='file'),
                            html.Div([
                                html.Div("Choose Image", className='fw-normal text-dark mb-1'),
                                html.Div("JPG, GIF or PNG. Max size of 800K", className='text-gray small')
                            ], className='d-md-block text-left')
                        ], className='d-flex')
                    ], className='d-flex justify-content-xl-center ms-xl-3')
                ], className='file-field')
            ], className='d-flex align-items-center')
        ], className='card card-body border-0 shadow mb-4')
    ], className='col-12')


def coverPhotoCard():
    return html.Div([
        html.Div([
            html.H2("Select cover photo", className='h5 mb-4'),
            html.Div([
                html.Div([
                    # Avatar
                    html.Img(className='rounded avatar-xl', src='../assets/img/profile-cover.jpg', alt='change cover')
                ], className='me-3'),
                html.Div([
                    html.Div([
                        html.Div([
                            PAPER_CLIP,
                            dcc.Input(type='file'),
                            html.Div([
                                html.Div("Choose Image", className='fw-normal text-dark mb-1'),
                                html.Div("JPG, GIF or PNG. Max size of 800K", className='text-gray small')
                            ], className='d-md-block text-left')
                        ], className='d-flex')
                    ], className='d-flex justify-content-xl-center ms-xl-3')
                ], className='file-field')
            ], className='d-flex align-items-center')
        ], className='card card-body border-0 shadow')
    ], className='col-12')

