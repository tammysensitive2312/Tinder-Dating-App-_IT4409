from datetime import datetime

from base_service import AbstractBaseService
from flask_jwt_extended import create_access_token, create_refresh_token
from main.domain_layer import User, Profile


class UserService(AbstractBaseService):
    def __init__(self, uow, logger):
        super().__init__(uow, logger)

    def get_user(self, user_id):
        user = self.uow.user_repository.get_user(user_id)
        return user

    def register_user(self, email: str, password: str, name: str) -> dict[str, str]:
        try:
            with self.uow:
                if self.uow.users.find_by_email(email):
                    raise ValueError("Email already exists")

                new_user = User(
                    email=email,
                    passwordHash=self.__hash_password(password),
                    isActive=True,
                    createdAt=datetime.now()
                )

                self.uow.users.add(new_user)

                new_profile = Profile(
                    userId=new_user.Id,
                    username=name,
                    createdAt=datetime.now()
                )
                self.uow.profiles.add(new_profile)

                identity = {
                    "user_id": new_user.Id,
                    "email": email
                }

                access_token = create_access_token(identity=identity)
                refresh_token = create_refresh_token(identity=identity)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": new_user.Id
                }
        except Exception as e:
            self.logger.error(f"Error registering user {e}")
            raise e


    def __hash_password(self, password: str) -> str:
        import hashlib
        password_hash = hashlib.md5(password.encode()).hexdigest()
        return  password_hash