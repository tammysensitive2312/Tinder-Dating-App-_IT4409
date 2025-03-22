from pydantic import BaseModel, EmailStr, constr
from flask import jsonify


STATUS_CODES = {
    "1000": "OK",
    "9992": "Post is not existed",
    "9993": "Code verify is incorrect",
    "9994": "No Data or end of list data",
    "9995": "User is not validated",
    "9996": "User existed",
    "9997": "Method is invalid",
    "9998": "Token is invalid",
    "9999": "Exception error",
    "1001": "Can not connect to DB",
    "1002": "Parameter is not enough",
    "1003": "Parameter type is invalid",
    "1004": "Parameter value is invalid",
    "1005": "Unknown error",
    "1006": "File size is too big",
    "1007": "Upload File Failed!",
    "1008": "Maximum number of images",
    "1009": "Not access",
    "1010": "Action has been done previously by this user"
}

class ApiResponse(BaseModel):
    status_code: str
    message: str
    data: dict

    def to_json(self):
        return jsonify(self.dict())

class SignupRequestDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    name: constr(min_length=2, max_length=50)

class SignupResponseDTO(BaseModel):
    id: str
    access_token: str
    refresh_token: str