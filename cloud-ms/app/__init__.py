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
	app = Flask(__name__)
	cfg = config[config_name]
	app.config.from_object(cfg)
	cfg.init_app(app)
	bootstrap.init_app(app)
	csrf.init_app(app)
	db.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
