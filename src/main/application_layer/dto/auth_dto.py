from pydantic import BaseModel, EmailStr, constr

class SignupRequestDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    name: constr(min_length=2, max_length=50)

class SignupResponseDTO(BaseModel):
    id: str
    access_token: str
    refresh_token: str