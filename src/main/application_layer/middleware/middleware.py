from abc import ABC
from datetime import time

from flask import request, g, jsonify
from flask_jwt_extended import decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from main.application_layer.pylog import PyLogger


class Middleware(ABC):
    pass

class LoggingMiddleware(Middleware):
    def __init__(self, app):
        self.app = app
        self.logger = PyLogger()
        self.register_middleware()

    def register_middleware(self):
        @self.app.before_request
        def start_timer():
            g.start_time = time.time()

        @self.app.after_request
        def log_request(response):
            end_time = time.time()
            duration = end_time - g.start_time
            token = request.headers.get('Authorization', 'No token')
            uri = request.path
            status_code = response.status_code
            log_message = f"URI: {uri}, Token: {token}, Status: {status_code}, Time: {duration:.4f}s"
            self.logger.info(log_message)
            return response


class AuthMiddleware(Middleware):
    def __init__(self, app):
        self.app = app
        self.logger = PyLogger()
        self.register_middleware()

    def register_middleware(self):
        @self.app.before_request
        def check_auth():
            token = request.headers.get('Authorization')
            if not token or not self.validate_token(token):
                return jsonify({"error": "Unauthorized"}), 401

    # def validate_token(self, token):
    #     if not token or not token.startswith("Bearer "):
    #         return False, "Invalid token format"
    #
    #     token = token[7:]
    #
    #     try:
    #         decoded_token = decode_token(token)
    #         user_id = decoded_token["sub"]["user_id"]
    #
    #         user = self.uow.users.get_by_id(user_id)
    #         if not user:
    #             return False, "User not found"
    #
    #         if not user.isActive:
    #             return False, "User account is disabled"
    #
    #         return True, decoded_token
    #
    #     except ExpiredSignatureError:
    #         return False, "Token has expired"
    #     except InvalidTokenError:
    #         return False, "Invalid token"
    #     except Exception as e:
    #         return False, f"Error validating token: {str(e)}"