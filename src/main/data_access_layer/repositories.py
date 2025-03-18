from sqlalchemy.orm import joinedload

from main.data_access_layer.strategies import QueryStrategy
from main.domain_layer import IUserRepository, IProfileRepository, ISwipeRepository, IQueryStrategy
from main.domain_layer import User, Profile, Swipe

class BaseRepository:
    def __init__(self, session):
        self.session = session
        self._strategies = []

    def add_filter_strategy(self, strategy: QueryStrategy):
        self._strategies.append(strategy)

    def _apply_strategies(self, query):
        for strategy in self._strategies:
            query = strategy.apply(query)
        return query

class UserRepository(BaseRepository, IUserRepository):
    def get_by_id(self, id: int) -> User:
        return self.session.query(User).get(id)

    def find_active_users(self) -> list[User]:
        query = self.session.query(User)
        query = self._apply_strategies(query)
        return query.filter(User.isActive == True).all()

    def get_with_profile(self, user_id: int) -> User:
        return self.session.query(User).\
            options(joinedload(User.profile)).\
            filter(User.Id == user_id).\
            first()

class ProfileRepository(BaseRepository, IProfileRepository):
    def update_bio(self, user_id: int, new_bio: str):
        profile = self.session.query(Profile).\
            filter(Profile.userId == user_id).\
            first()
        if profile:
            profile.bio = new_bio
            self.session.commit()

    def get_with_photos(self, profile_id: int) -> Profile:
        return self.session.query(Profile).\
            options(joinedload(Profile.photos)).\
            filter(Profile.Id == profile_id).\
            first()

class SwipeRepository(BaseRepository, ISwipeRepository):
    def get_recent_swipes(self, user_id: int, days: int) -> list[Swipe]:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=days)
        return self.session.query(Swipe).\
            filter(Swipe.swiperId == user_id).\
            filter(Swipe.createdAt >= cutoff).\
            all()

    def get_mutual_swipes(self, user1_id: int, user2_id: int) -> list[Swipe]:
        return self.session.query(Swipe).\
            filter(
                ((Swipe.swiperId == user1_id) & (Swipe.swipedId == user2_id)) |
                ((Swipe.swiperId == user2_id) & (Swipe.swipedId == user1_id))
            ).all()