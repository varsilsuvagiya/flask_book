from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config.from_pyfile('../config.py')
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)

from app import routes, models
