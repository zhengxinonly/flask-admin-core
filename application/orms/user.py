from werkzeug.security import check_password_hash, generate_password_hash

from application.extensions import db


class UserORM(db.Model):
    __tablename__ = "ums_user"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    no = db.Column(db.String(8))

    @property
    def password(self):
        raise Exception("禁止直接访问密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)
