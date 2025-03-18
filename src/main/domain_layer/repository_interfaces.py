from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')

class IRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        pass

class IQueryStrategy(ABC):
    @abstractmethod
    def apply(self, query):
        pass

class BaseRepository(IRepository, ABC):
    def __init__(self, db):
        self.db = db

    def add_strategy(self, strategy: IQueryStrategy):
        pass

    def remove_strategy(self, strategy_type: type):
        pass

    @abstractmethod
    def get_base_query(self):
        pass

class IUserRepository(BaseRepository):
    @abstractmethod
    def find_by_email(self, email: str):
        pass

    @abstractmethod
    def find_active_users(self):
        pass

    @abstractmethod
    def get_with_profile(self, user_id: int):
        pass

class IProfileRepository(BaseRepository):
    @abstractmethod
    def update_bio(self, user_id: int, new_bio: str):
        pass

    @abstractmethod
    def get_with_photos(self, profile_id: int):
        pass

class ISwipeRepository(BaseRepository):
    @abstractmethod
    def get_recent_swipes(self, user_id: int, days: int):
        pass

    @abstractmethod
    def get_mutual_swipes(self, user1_id: int, user2_id: int):
        pass