import os

def get_env(key):
    return os.environ.get('SECRET_KEY', None)

class Config:
    SECRET_KEY = get_env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI')

    @classmethod
    def init_app(cls, app):
        pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}