from flask import Flask
from flask_bootstrap import Bootstrap
from config import config
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
	cfg = config[config_name]
	app = Flask(__name__)
	bootstrap.init_app(app)
	db.init_app(app)
	cfg.init_app(app)
	csrf.init_app(app)
	app.config.from_object(cfg)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
