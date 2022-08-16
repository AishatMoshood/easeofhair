class Config(object):
    ADMIN_EMAIL = 'info@easeofhair.com'
    USERNAME = 'Ease of Hair'
    PASSWORD = 'password'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vqttegkclapauk:c86eb9b30ee0484d0b45d9b4be528280b3fd1c8c8395ea9e99ac09a4914731e2@ec2-44-207-126-176.compute-1.amazonaws.com:5432/dfgqhg2d345bbs'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MERCHANT_ID = 't98765@0'

class TestConfig(Config):
    DATABASE_URI = 'Test Connection parameters'
