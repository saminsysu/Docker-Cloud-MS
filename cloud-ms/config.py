import os

def get_env(key):
    return os.environ.get(key, None)

class Config:
    SECRET_KEY = get_env('SECRET_KEY')

    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}