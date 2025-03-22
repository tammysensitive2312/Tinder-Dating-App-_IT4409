from main.data_access_layer.repositories import UserRepository, ProfileRepository, SwipeRepository
from contextlib import contextmanager


class UnitOfWork:
    def __init__(self, db_context):
        self.db_context = db_context  # Giữ reference đến SqlAlchemyDbContext

    @contextmanager
    def start(self):
        """Tạo session và quản lý transaction tự động."""
        session = self.db_context.Session()  # Tạo session mới
        try:
            # Khởi tạo repository với session hiện tại
            self.users = UserRepository(session)
            self.profiles = ProfileRepository(session)
            self.swipes = SwipeRepository(session)
            self.session = session
            yield self  # Trả về UoW để sử dụng trong with block
            session.commit()  # Tự động commit nếu không có exception
        except Exception as e:
            session.rollback()  # Rollback nếu có lỗi
            raise e
        finally:
            session.close()  # Đảm bảo session luôn được đóng

    def flush(self):
        """Explicitly flush session to generate IDs."""
        self.session.flush()
