from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("settings.py")

db = SQLAlchemy(app)

from . import models
from . import views