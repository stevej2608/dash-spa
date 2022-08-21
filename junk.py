from dash_spa.logging import setLevel, log
from werkzeug.local import LocalProxy
import time

active = False

class


def register_page():

    def _register_page():
        return 1

    return LocalProxy(_register_page)




if __name__ == "__main__":
    setLevel("INFO")
    page = register_page()
