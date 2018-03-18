import os
basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ['APP_SETTINGS'] == 'confir.DevelopmentConfig':
    from secretkey import SECRET


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    if os.environ['APP_SETTINGS'] == 'config.DevelopmentConfig':
        SECRET_KEY = SECRET
    else:
        SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
