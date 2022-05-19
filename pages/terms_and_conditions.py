from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_spa import register_page

from pages import TERMS_AND_CONDITIONS_SLUG

register_page(__name__, path=TERMS_AND_CONDITIONS_SLUG, title="Dash Solar", short_name='Licence')

layout = html.Div([
        html.H2('Terms and Conditions'),
        html.P("Aliquip excepteur anim aliqua amet velit qui aute."),
        html.P("Amet in excepteur adipisicing duis ad est amet aliquip duis et et non. Do laborum aliqua deserunt ipsum pariatur exercitation ipsum nulla mollit ullamco nisi consequat esse veniam. Esse exercitation aliqua sunt magna duis occaecat sunt ipsum officia laborum. Ex labore nisi dolor quis quis ex elit quis laboris ut non tempor. Mollit deserunt eiusmod est adipisicing do aliqua nulla sint qui."),
        html.P("Excepteur sint amet incididunt culpa irure consectetur exercitation ad sunt. Sunt aliqua anim aliqua non dolor do. Nostrud nisi commodo dolor sint quis reprehenderit mollit. Eu nulla sunt eu sint excepteur nulla officia commodo eiusmod eu tempor."),
        html.P("Eu excepteur esse nostrud fugiat voluptate nostrud cupidatat amet tempor velit mollit sint do voluptate. Exercitation excepteur Lorem adipisicing enim. Consectetur excepteur ex ullamco quis exercitation aliquip cupidatat excepteur laboris.")
    ])
