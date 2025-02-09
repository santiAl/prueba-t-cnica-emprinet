from decouple import config


class Config():
    SECREAT_KEY = config('SECRET_KEY')  # Lee desde el archivo .env o desde docker-compose.yml


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')  # Lee desde el archivo .env o desde docker-compose.yml

config = {
    'development': DevelopmentConfig
}