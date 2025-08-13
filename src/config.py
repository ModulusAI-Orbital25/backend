from os import environ


class Config(object):
    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = environ.get("POSTGRES_DB")
    POSTGRES_NAME = environ.get("POSTGRES_NAME")

    # SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_NAME}:5432/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

    SECRET_KEY = environ.get("SECRET_KEY")

    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
