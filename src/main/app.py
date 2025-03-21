from flask import Flask
from main.application_layer.container import AppContainer
from main.application_layer.routing.routes import setup_router

def run_server_engine():
    app = Flask(__name__)
    container = AppContainer()
    setup_router(app, container)

if __name__ == '__main__':
    app = run_server_engine()
    app.run(port=5000, debug=True)