from decouple import config


class Config():
    SECREAT_KEY = config('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')  # Lee desde el archivo .env

config = {
    'development': DevelopmentConfig
}