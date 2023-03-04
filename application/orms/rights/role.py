from datetime import datetime

from application.extensions import db


class RoleORM(db.Model):
    __tablename__ = "ums_role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, comment="角色名称")
    code = db.Column(db.String(20), nullable=False, comment="角色识别码")
    desc = db.Column(db.Text, nullable=True, comment="角色描述")

    permission_code_list = db.Column(
        db.String(512),
        nullable=True,
        comment="权限ids 1:2:5。冗余字段，用户缓存用户权限",
    )

    permission_list = db.relationship(
        "PermissionORM",
        secondary="ums_role_permission",
        back_populates="role_list",
    )

    user_list = db.relationship(
        "UserORM",
        secondary="ums_user_role",
        back_populates="role_list",
    )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"id": self.id, "name": self.name, "code": self.code, "desc": self.desc}
