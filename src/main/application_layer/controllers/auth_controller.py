from flask import request
from pydantic import ValidationError

from main.application_layer.DTOs.auth_dto import SignupRequestDTO, SignupResponseDTO, ApiResponse, STATUS_CODES, \
    LoginRequestDTO, ResetPasswordRequestDTO, ChangePasswordRequestDTO
from main.application_layer.controllers.base import BaseController
from main.application_layer.pylog import PyLogger as log
from main.use_case_layer.user_service import UserService


class AuthController(BaseController):
    def __init__(self, auth_service: UserService, logger: log):
        super().__init__(logger)
        self.auth_service = auth_service

    def register(self):
        try:
            user_data = SignupRequestDTO(**request.json)

            result = self.auth_service.register_user(
                email=user_data.email,
                password=user_data.password,
                name=user_data.name
            )

            response_data = SignupResponseDTO(
                id=str(result["user_id"]),
                access_token=result["access_token"],
                refresh_token=result["refresh_token"]
            )

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data=response_data.model_dump()
            )

            return api_response.to_json(), 201

        except ValidationError as e:
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except ValueError as e:
            api_response = ApiResponse(
                status_code="9996" if "Email already exists" in str(e) else "1004",
                message=STATUS_CODES["9996"] if "Email already exists" in str(e) else STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except Exception as e:
            self.log.error(f"Error registering user {e}")
            api_response = ApiResponse(
                status_code="9999",  # Exception error
                message=STATUS_CODES["9999"],
                data={"error": "Internal server error"}
            )
            return api_response.to_json(), 500


    def login(self):
        try:
            user_data = LoginRequestDTO(**request.json)

            result = self.auth_service.login(
                email=user_data.email,
                password=user_data.password,
            )

            response_data = SignupResponseDTO(
                id=str(result["user_id"]),
                access_token=result["access_token"],
                refresh_token=result["refresh_token"]
            )

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data=response_data.model_dump()
            )

            return api_response.to_json(), 200

        except ValidationError as e:
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except ValueError as e:
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except Exception as e:
            self.log.error(f"Error login user {e}")
            api_response = ApiResponse(
                status_code="9999",
                message=STATUS_CODES["9999"],
                data={"error": "Internal server error"}
            )
            return api_response.to_json(), 500


    def refresh_token(self):
        try:
            refresh_token = request.json.get("refresh_token")
            self.log.info(f"Refresh token in controller : {refresh_token}")
            if not refresh_token:
                raise ValueError("Refresh token is required")

            new_access_token = self.auth_service.refresh_token(refresh_token)

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data={"access_token": new_access_token}
            )

            return api_response.to_json(), 200

        except ValueError as e:
            api_response = ApiResponse(
                status_code="9998",
                message=STATUS_CODES["9998"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except Exception as e:
            self.log.error(f"Error refreshing token {e}")
            api_response = ApiResponse(
                status_code="9999",
                message=STATUS_CODES["9999"],
                data={"error": "Internal server error"}
            )
            return api_response.to_json(), 500


    def reset_password(self):
        try:
            email = request.json.get("email")
            self.auth_service.request_password_reset(email)

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data={"message": "Password reset link sent to email"}
            )

            return api_response.to_json(), 200

        except ValidationError as e:
            self.log.error(f"Error requesting password reset {e}")
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400

        except ValueError as e:
            self.log.error(f"Error requesting password reset {e}")
            api_response = ApiResponse(
                status_code="1005",
                message=STATUS_CODES["1005"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 500

    def confirm_reset_password(self):
        try:
            data = ResetPasswordRequestDTO(**request.json)
            self.auth_service.confirm_password_reset(data)

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data={"message": "Password reset successfully"}
            )

            return api_response.to_json(), 200

        except ValidationError as e:
            self.log.error(f"Error confirming password reset {e}")
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400


    def change_password(self):
        try:
            data = ChangePasswordRequestDTO(**request.json)
            email = data.email
            old_password = data.old_password
            new_password = data.new_password

            response = self.auth_service.change_password(email, old_password, new_password)

            api_response = ApiResponse(
                status_code="1000",
                message=STATUS_CODES["1000"],
                data=response
            )

            return api_response.to_json(), 200

        except ValidationError as e:
            self.log.error(f"Error changing password {e}")
            api_response = ApiResponse(
                status_code="1004",
                message=STATUS_CODES["1004"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 400
        except Exception as e:
            self.log.error(f"Error changing password {e}")
            api_response = ApiResponse(
                status_code="1005",
                message=STATUS_CODES["1005"],
                data={"error": str(e)}
            )
            return api_response.to_json(), 500