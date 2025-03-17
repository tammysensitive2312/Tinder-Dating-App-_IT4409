from flask import Flask
from flask_migrate import Migrate

from config import Config
from models import db
from routes import api, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
api.init_app(app)
jwt.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
