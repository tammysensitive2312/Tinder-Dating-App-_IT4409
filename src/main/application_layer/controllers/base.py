from main.application_layer.pylog import PyLogger as log

class BaseController:
    def __init__(self, logger: log):
        self.log = logger