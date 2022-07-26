
class SessionBackend:

    def get(self, obj_key) -> dict:
        raise NotImplementedError

    def set(self, obj_key, value: dict):
        raise NotImplementedError





