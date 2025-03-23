import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt
import pyotp
from pydantic.v1 import EmailStr

from main.use_case_layer.base_service import AbstractBaseService
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from main.domain_layer import User, Profile

otp_storage = {}

class UserService(AbstractBaseService):

    def __init__(self, uow, logger):
        super().__init__(uow, logger)

    def register_user(self, email: EmailStr, password: str, name: str) -> dict[str, str, int]:
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

                uow.users.add(new_user)
                uow.flush()

                new_profile = Profile(
                    userId=new_user.Id,
                    username=name,
                    createdAt=datetime.now()
                )

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


    def login(self, email: EmailStr, password: str) -> dict[str, str, int]:
        try:
            with self.uow.start() as uow:
                user = uow.users.find_by_email(email)
                if user is None:
                    raise ValueError("Email does not exist")

                if not self.__verify_password(password, user.passwordHash):
                    raise ValueError("Password is incorrect")

                identity = {
                    "user_id": user.Id,
                    "email": email
                }

                access_token = create_access_token(identity=identity)
                refresh_token = create_refresh_token(identity=identity)

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": user.Id
                }
        except Exception as e:
            self.logger.error(f"Error logging in user {e}")
            raise e


    def refresh_token(self, refresh_token: str) -> str:
        self.logger.info(f"Refresh token in service : {refresh_token}")

        decoded_token = decode_token(refresh_token)
        user_id = decoded_token["sub"]["user_id"]

        self.logger.info(f"Decoded token: {decoded_token}")
        self.logger.info(f"User ID: {user_id}")

        try:
            with self.uow.start() as uow:
                user = uow.users.get_by_id(user_id)
                if user is None:
                    raise ValueError("User does not exist")

                identity = {
                    "user_id": user.Id,
                    "email": user.email
                }

                access_token = create_access_token(identity=identity)

                return access_token
        except Exception as e:
            self.logger.error(f"Error refreshing token {e}")
            raise e


    def request_password_reset(self, email: str) -> dict:
        try:
            with self.uow.start() as uow:
                user = uow.users.find_by_email(email)
                if user is None:
                    raise ValueError("Email does not exist")

                otp_secret = pyotp.random_base32()
                otp = pyotp.TOTP(otp_secret, interval=300).now()
                otp_expiry = datetime.now()+ timedelta(minutes=5)

                otp_storage[email] = {
                    "otp_secret": otp_secret,
                    "otp_expiry": otp_expiry
                }

                self.__send_otp_email(email, otp)

                return {
                    "otp_expiry": otp_expiry.isoformat()
                }
        except Exception as e:
            self.logger.error(f"Error requesting password reset {e}")
            raise e

    def __send_otp_email(self, email: str, otp: str):
        sender_email = "dinhtruong1234lhp@gmail.com"
        sender_password = " "
        subject = "Mã OTP đặt lại mật khẩu"
        body = f"Mã OTP của bạn là: {otp}. Mã có hiệu lực trong 5 phút."

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, message.as_string())
            self.logger.info(f"OTP sent to {email}")
        except Exception as e:
            self.logger.error(f"Error sending OTP email: {e}")
            raise e

    def confirm_password_reset(self, email: str, otp: str, new_password: str) -> dict:
        try:
            with self.uow.start() as uow:

                if email not in otp_storage:
                    raise ValueError("OTP không hợp lệ hoặc đã hết hạn")

                otp_info = otp_storage[email]
                otp_secret = otp_info["otp_secret"]
                otp_expiry = otp_info["otp_expiry"]

                if datetime.now() > otp_expiry:
                    del otp_storage[email]
                    raise ValueError("OTP đã hết hạn")

                totp = pyotp.TOTP(otp_secret, interval=300)
                if not totp.verify(otp):
                    raise ValueError("OTP không hợp lệ")

                user = uow.users.find_by_email(email)
                if user is None:
                    raise ValueError("Email không tồn tại")

                user.passwordHash = self.__hash_password(new_password)

                del otp_storage[email]

                return {
                    "status": "success"
                }
        except Exception as e:
            self.logger.error(f"Error confirming password reset: {e}")
            raise e


    def change_password(self, user_email: str, old_password: str, new_password: str) -> dict:
        try:
            with self.uow.start() as uow:
                user = uow.users.find_by_email(user_email)
                if user is None:
                    raise ValueError("User does not exist")

                if not self.__verify_password(old_password, user.passwordHash):
                    raise ValueError("Old password is incorrect")

                user.passwordHash = self.__hash_password(new_password)

                return {
                    "status": "success"
                }
        except Exception as e:
            self.logger.error(f"Error changing password: {e}")
            raise e

    @staticmethod
    def __hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def __verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))