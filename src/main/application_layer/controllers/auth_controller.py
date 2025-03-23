from flask import request
from pydantic import ValidationError

from main.application_layer.DTOs.auth_dto import SignupRequestDTO, SignupResponseDTO, ApiResponse, STATUS_CODES
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