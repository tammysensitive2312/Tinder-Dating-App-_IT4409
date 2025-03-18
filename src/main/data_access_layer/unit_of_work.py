from contextlib import contextmanager

from main.data_access_layer import UserRepository, ProfileRepository, SwipeRepository


class UnitOfWork:
    def __init__(self, db_context):
        self.db_context = db_context
        self.session = db_context.Session()

    def __enter__(self):
        self.users = UserRepository(self.session)
        self.profiles = ProfileRepository(self.session)
        self.swipes = SwipeRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
