from dash import html, dcc
from ..icons import CALENDER


def generalInformationForm():
    return html.Div([
        html.H2("General information", className='h5 mb-4'),
        html.Form([
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("First Name", htmlFor='first_name'),
                        dcc.Input(className='form-control', id='first_name', type='text', placeholder='Enter your first name', required='')
                    ])
                ], className='col-md-6 mb-3'),
                html.Div([
                    html.Div([
                        html.Label("Last Name", htmlFor='last_name'),
                        dcc.Input(className='form-control', id='last_name', type='text', placeholder='Also your last name', required='')
                    ])
                ], className='col-md-6 mb-3')
            ], className='row'),
            html.Div([
                html.Div([
                    html.Label("Birthday", htmlFor='birthday'),
                    html.Div([
                        html.Span(CALENDER, className='input-group-text'),
                        dcc.Input(className='form-control', id='birthday', type='text', placeholder='dd/mm/yyyy', required='')
                    ], className='input-group')
                ], className='col-md-6 mb-3'),
                html.Div([
                    html.Label("Gender", htmlFor='gender'),
                    html.Select([
                        html.Option("Gender", selected=''),
                        html.Option("Female", value='1'),
                        html.Option("Male", value='2')
                    ], className='form-select mb-0', id='gender', **{"aria-label": "Gender select example"})
                ], className='col-md-6 mb-3')
            ], className='row align-items-center'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Email", htmlFor='email'),
                        dcc.Input(className='form-control', id='email', type='email', placeholder='name@company.com', required='')
                    ], className='form-group')
                ], className='col-md-6 mb-3'),
                html.Div([
                    html.Div([
                        html.Label("Phone", htmlFor='phone'),
                        dcc.Input(className='form-control', id='phone', type='number', placeholder='+12-345 678 910', required='')
                    ], className='form-group')
                ], className='col-md-6 mb-3')
            ], className='row'),
            html.H2("Location", className='h5 my-4'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Address", htmlFor='address'),
                        dcc.Input(className='form-control', id='address', type='text', placeholder='Enter your home address', required='')
                    ], className='form-group')
                ], className='col-sm-9 mb-3'),
                html.Div([
                    html.Div([
                        html.Label("Number", htmlFor='number'),
                        dcc.Input(className='form-control', id='number', type='number', placeholder='No.', required='')
                    ], className='form-group')
                ], className='col-sm-3 mb-3')
            ], className='row'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("City", htmlFor='city'),
                        dcc.Input(className='form-control', id='city', type='text', placeholder='City', required='')
                    ], className='form-group')
                ], className='col-sm-4 mb-3'),
                html.Div([
                    html.Label("State", htmlFor='state'),
                    html.Select([
                        html.Option("State", selected=''),
                        html.Option("Alabama", value='AL'),
                        html.Option("Alaska", value='AK'),
                        html.Option("Arizona", value='AZ'),
                        html.Option("Arkansas", value='AR'),
                        html.Option("California", value='CA'),
                        html.Option("Colorado", value='CO'),
                        html.Option("Connecticut", value='CT'),
                        html.Option("Delaware", value='DE'),
                        html.Option("District Of Columbia", value='DC'),
                        html.Option("Florida", value='FL'),
                        html.Option("Georgia", value='GA'),
                        html.Option("Hawaii", value='HI'),
                        html.Option("Idaho", value='ID'),
                        html.Option("Illinois", value='IL'),
                        html.Option("Indiana", value='IN'),
                        html.Option("Iowa", value='IA'),
                        html.Option("Kansas", value='KS'),
                        html.Option("Kentucky", value='KY'),
                        html.Option("Louisiana", value='LA'),
                        html.Option("Maine", value='ME'),
                        html.Option("Maryland", value='MD'),
                        html.Option("Massachusetts", value='MA'),
                        html.Option("Michigan", value='MI'),
                        html.Option("Minnesota", value='MN'),
                        html.Option("Mississippi", value='MS'),
                        html.Option("Missouri", value='MO'),
                        html.Option("Montana", value='MT'),
                        html.Option("Nebraska", value='NE'),
                        html.Option("Nevada", value='NV'),
                        html.Option("New Hampshire", value='NH'),
                        html.Option("New Jersey", value='NJ'),
                        html.Option("New Mexico", value='NM'),
                        html.Option("New York", value='NY'),
                        html.Option("North Carolina", value='NC'),
                        html.Option("North Dakota", value='ND'),
                        html.Option("Ohio", value='OH'),
                        html.Option("Oklahoma", value='OK'),
                        html.Option("Oregon", value='OR'),
                        html.Option("Pennsylvania", value='PA'),
                        html.Option("Rhode Island", value='RI'),
                        html.Option("South Carolina", value='SC'),
                        html.Option("South Dakota", value='SD'),
                        html.Option("Tennessee", value='TN'),
                        html.Option("Texas", value='TX'),
                        html.Option("Utah", value='UT'),
                        html.Option("Vermont", value='VT'),
                        html.Option("Virginia", value='VA'),
                        html.Option("Washington", value='WA'),
                        html.Option("West Virginia", value='WV'),
                        html.Option("Wisconsin", value='WI'),
                        html.Option("Wyoming", value='WY')
                    ], className='form-select w-100 mb-0', id='state', name='state', **{"aria-label": "State select example"})
                ], className='col-sm-4 mb-3'),
                html.Div([
                    html.Div([
                        html.Label("ZIP", htmlFor='zip'),
                        dcc.Input(className='form-control', id='zip', type='tel', placeholder='ZIP', required='')
                    ], className='form-group')
                ], className='col-sm-4')
            ], className='row'),
            html.Div([
                html.Button("Save all", className='btn btn-gray-800 mt-2 animate-up-2', type='submit')
            ], className='mt-3')
        ])
    ], className='card card-body border-0 shadow mb-4')
