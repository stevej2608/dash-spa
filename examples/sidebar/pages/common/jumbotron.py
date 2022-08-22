from dash import html

def big_center(text):
    return html.H2(text, className='display-3 text-center')

def jumbotron_content(header, message=""):

    return html.Div(
        html.Header([
            big_center(header),
            big_center(message)
        ], className='jumbotron my-4')

    )
