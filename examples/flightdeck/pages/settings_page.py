import logging
from dash import html
from dash_spa import register_page

from .common import sideBar, mobileNavBar, topNavBar, footer, buttonBar
from .settings import userPhotoCard, profilePhotoCard, coverPhotoCard, generalInformationForm, alertsNotifications, reportsDropdown, newButton, calenderButton


register_page(__name__, path="/pages/settings.html", title="Dash/Flightdeck - Settings")

layout = html.Div([
    mobileNavBar(),
    sideBar(),

    html.Main([
        topNavBar(),
        buttonBar(
            lhs=newButton(),
            rhs = [
                calenderButton(),
                reportsDropdown()
            ]
        ),
        html.Div([
            html.Div([
                generalInformationForm(),
                alertsNotifications()
            ], className='col-12 col-xl-8'),
            html.Div([
                html.Div([
                    userPhotoCard(),
                    profilePhotoCard(),
                    coverPhotoCard(),
                ], className='row')
            ], className='col-12 col-xl-4')
        ], className='row'),
        # settingsPopupPanel(),
        # settingsPopupButton(),
        footer()
    ], className='content')
])
