import dash_bootstrap_components as dbc
from dash_spa import DashSPA

# Note: The location of this module defines the Dash/SPA
# app root. Unless specified otherwise Dash/SPA will
# expect the 'pages' and 'assets' folders to be
# child folders off this root.

app = DashSPA( __name__,external_stylesheets=[dbc.themes.BOOTSTRAP])