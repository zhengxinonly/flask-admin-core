import os


class Base:
    ROOT_PATH = os.path.dirname(__file__)
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 3306

    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "root"
    MYSQL_DB = "flask_admin"

    SECRET_KEY = os.urandom(16)

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PWD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"


class Development(Base):
    CONFIG_NAME = "dev"


class Tester(Base):
    CONFIG_NAME = "test"


class Production(Base):
    CONFIG_NAME = "prod"


config_dict = {
    "dev": Development(),
    "test": Tester(),
    "prod": Production(),
}
