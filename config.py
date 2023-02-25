import os


class Base:
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 3306

    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PWD = "root"
    MYSQL_DB = ""

    SECRET_KEY = os.urandom(16)

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PWD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"


class Development(Base):
    pass


class Tester(Base):
    pass


class Production(Base):
    pass


config_dict = {
    "dev": Development(),
    "test": Tester(),
    "prod": Production(),
}
