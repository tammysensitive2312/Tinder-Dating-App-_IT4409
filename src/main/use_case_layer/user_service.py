from datetime import datetime

import bcrypt

from main.use_case_layer.base_service import AbstractBaseService
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
            with self.uow.start() as uow:
                if uow.users.find_by_email(email):
                    raise ValueError("Email already exists")

                new_user = User(
                    email=email,
                    passwordHash=self.__hash_password(password),
                    isActive=True,
                    createdAt=datetime.now()
                )

                print("line 1 new_user:", new_user.__dict__)
                print("line 1 new_user.Id:", new_user.Id)

                uow.users.add(new_user)
                uow.flush()

                print("line 2 new_user:", new_user.__dict__)
                print("line 2 new_user.Id:", new_user.Id)

                new_profile = Profile(
                    userId=new_user.Id,
                    username=name,
                    createdAt=datetime.now()
                )

                print("new_profile:", new_profile.__dict__)
                uow.profiles.add(new_profile)

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
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def __verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))