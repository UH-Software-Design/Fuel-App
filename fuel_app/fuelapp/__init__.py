from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['SECRET_KEY'] = '9e844a33d2830730d50f1ba5f80ee4c844364'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)

from fuelapp import routes