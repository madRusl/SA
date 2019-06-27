from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

from app import routes, models, errors
