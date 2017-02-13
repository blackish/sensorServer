from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask ( __name__ )
app.debug = True
app.config [ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/src/sensors/sensors.db'
app.config.from_object ( 'config' )
db = SQLAlchemy ( app )

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import model, views
