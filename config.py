import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SLACK_API_KEY = os.environ['SLACK_API_KEY']
	SECRET_KEY = os.environ['SECRET_KEY']
	LUG_SECRET_KEY = osenviron['LUG_SECRET_KEY']
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
