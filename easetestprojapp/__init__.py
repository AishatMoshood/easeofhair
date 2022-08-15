from flask import Flask
import sys, logging
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

from easetestprojapp import config
app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)

mail = Mail(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from easetestprojapp.myroutes import adminroutes, userroutes, salonroutes
from easetestprojapp import forms, mymodels