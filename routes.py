from flask import request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, Api

from models import db, User

api = Api()

# Khởi tạo JWT
jwt = JWTManager()


class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists"}, 400

        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201


class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=str(user.id))  # Ép kiểu thành chuỗi
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401


# class UserProfileAPI(Resource):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if not user:
#             return {"message": "User not found"}, 404
#         return {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "gender": user.gender,
#             "bio": user.bio
#         }, 200


# Đăng ký API vào Flask-RESTful
api.add_resource(RegisterAPI, "/register")
api.add_resource(LoginAPI, "/login")
# api.add_resource(UserProfileAPI, "/profile")
