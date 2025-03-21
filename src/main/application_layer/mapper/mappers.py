from main.application_layer.dto.auth_dto import SignupRequestDTO, SignupResponseDTO
from main import User, Profile

class AuthMapper:
    @staticmethod
    def to_entity(dto: SignupRequestDTO) -> tuple[User, Profile]:
        user = User(
            email=dto.email,
            passwordHash=dto.password  # Will be hashed in service
        )
        profile = Profile(
            username=dto.name
        )
        return user, profile