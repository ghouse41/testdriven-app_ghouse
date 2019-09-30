import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG_TB_ENABLED = False 
    DEBUG_TB_INTERCEPT_REDIRECTS = False 
    BCRYPT_LOG_ROUNDS = 13
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION_DAYS = 30 # new
    TOKEN_EXPIRATION_SECONDS = 0 # new
    ADMINS = ['shaikm12@gmail.com']
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True # new
    BCRYPT_LOG_ROUNDS = 4

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0 # new
    TOKEN_EXPIRATION_SECONDS = 3 # new


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
