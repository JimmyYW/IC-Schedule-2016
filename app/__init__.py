from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# from app import views, models !!This line from last year
# must go at end of file to avoid import loop.
from app import models
# TODO: implement views.py and import here

