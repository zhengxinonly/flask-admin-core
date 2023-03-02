from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from application.extensions import db


class UserORM(db.Model):
    __tablename__ = "ums_user"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    mobile = db.Column(db.String(11))
    create_at = db.Column(
        db.DateTime,
        nullable=False,
        comment="创建时间",
        default=datetime.now,
    )

    role_list = db.relationship(
        "RoleORM",
        secondary="ums_user_role",
        back_populates="user_list",
    )

    @property
    def password(self):
        raise Exception("禁止直接访问密码")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    @classmethod
    def find_by_username(cls, nickname):
        return cls.query.filter_by(username=nickname).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
