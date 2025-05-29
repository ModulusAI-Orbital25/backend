from os import environ

class Config(object):
    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = environ.get("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
