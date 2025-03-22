from flask import request, jsonify, Response
from pydantic import ValidationError
from main.use_case_layer.user_service import UserService
from main.application_layer.dto.auth_dto import SignupRequestDTO, SignupResponseDTO
from main.application_layer.pylog import PyLogger as log


class AuthController:
    def __init__(self, auth_service: UserService, logger: log):
        self.auth_service = auth_service
        self.log = logger

    def register(self):
        try:
            user_data = SignupRequestDTO(**request.json)

            print("user_data.email:", user_data.email)
            print("user_data.password:", user_data.password)
            print("user_data.name:", user_data.name)

            result = self.auth_service.register_user(
                email=user_data.email,
                password=user_data.password,
                name=user_data.name
            )

            print("result:", result)

            response_data = SignupResponseDTO(
                id=str(result["user_id"]),
                access_token=result["access_token"],
                refresh_token=result["refresh_token"]
            )
            return Response(response_data.json(), mimetype="application/json"), 201

        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            self.log.error(f"Error registering user {e}")
            return jsonify({"error": "Internal server error"}), 500