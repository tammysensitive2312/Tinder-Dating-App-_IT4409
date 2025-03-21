from main.data_access_layer import UnitOfWork
from main.application_layer.pylog import PyLogger

class AbstractBaseService:
    def __init__(self, uow: UnitOfWork, logger: PyLogger):
        self.uow = uow
        self.logger = logger