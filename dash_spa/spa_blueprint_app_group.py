from flask.cli import AppGroup

class BlueprintAppGroup(AppGroup):
    """Flag cli commands are defined by blueprint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasCommand = False

    def command(self, *args, **kwargs):
        self.hasCommand = True
        return super().command(*args, **kwargs)