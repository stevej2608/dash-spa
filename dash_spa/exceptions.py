from dash.exceptions import DashException

class InvalidUsageException(DashException):
    pass


class InvalidAccess(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
