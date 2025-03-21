from flask import request, jsonify
from pydantic import ValidationError
from main.use_case_layer.user_service import UserService
from main.application_layer.dto.auth_dto import SignupRequestDTO, SignupResponseDTO


class AuthController:
    def __init__(self, auth_service: UserService):
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
            return jsonify(response_data), 201

        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500