from flask import Flask
import sys, logging
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from easetestprojapp import config
app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from easetestprojapp.myroutes import adminroutes, userroutes, salonroutes
from easetestprojapp import forms, mymodels