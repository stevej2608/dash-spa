from app import create_dash
from usage import create_spa

def create_app():
    app = create_spa(create_dash)
    return app.dash.server

app = create_app()

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=8050)
