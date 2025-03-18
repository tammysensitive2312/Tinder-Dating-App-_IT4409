from abc import ABC, abstractmethod
from sqlalchemy.orm import Query

from main.domain_layer import Profile, User


class QueryStrategy(ABC):
    @abstractmethod
    def apply(self, query: Query) -> Query:
        pass


class GenderFilterStrategy(QueryStrategy):
    def __init__(self, gender):
        self.gender = gender

    def apply(self, query: Query) -> Query:
        return query.filter(Profile.gender == self.gender)


class LocationFilterStrategy(QueryStrategy):
    def __init__(self, coordinates, radius):
        self.coordinates = coordinates
        self.radius = radius

    def apply(self, query: Query) -> Query:
        return query

class ActivityFilterStrategy(QueryStrategy):
    def apply(self, query: Query) -> Query:
        return query.filter(User.isActive == True)