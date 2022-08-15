class Config(object):
    ADMIN_EMAIL = 'info@easeofhair.com'
    USERNAME = 'Ease of Hair'
    PASSWORD = 'password'

class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root@127.0.0.1/easetest'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MERCHANT_ID = 't98765@0'


class TestConfig(Config):
    DATABASE_URI = 'Test Connection parameters'
