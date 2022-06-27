from flask import Flask
from config import Config
from flask_admin import Admin
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restful import Api

app = Flask(__name__)
admin = Admin(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
cors = CORS(app, resources={r"*": {"origins": "*"}})
#login de miguel
login = LoginManager(app)
login.login_view = 'login'
api = Api(app)

from app import routes, models, routesapi

