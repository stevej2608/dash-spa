import dash
import dash_bootstrap_components as dbc

# Note: The location of this module defines the Dash/SPA
# app root. Unless specified otherwise Dash/SPA will
# expect the 'pages' and 'assets' folders to be
# child folders off this root.

app = dash.Dash( __name__,
        use_pages = True,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
        )