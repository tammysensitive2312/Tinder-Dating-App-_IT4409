from flask import Flask
from flask_jwt_extended import JWTManager

from .application_layer.container import AppContainer
from .application_layer.routing.routes import setup_router
from .application_layer.constants import JWT_SECRET_KEY, EXPIRATION_TIME, JWT_ALGORITHM


def run_server_engine():
    app = Flask(__name__)
    container = AppContainer()

    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = EXPIRATION_TIME
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = EXPIRATION_TIME * 5
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["jwt.algorithms.Algorithm"] = JWT_ALGORITHM
    print("JWT_SECRET_KEY trong app.py:", JWT_SECRET_KEY)

    jwt = JWTManager(app)

    db_context = container.infrastructure.db_context()
    db_context.init_db()

    setup_router(app, container)
    return app

if __name__ == '__main__':
    app = run_server_engine()
    app.run(port=5000, debug=True)