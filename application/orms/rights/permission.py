from application.extensions import db


class PermissionORM(db.Model):
    __tablename__ = "ums_permission"

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(20), nullable=False, comment="权限名称")
    permission_code = db.Column(db.String(30), comment="权限标识")
    permission_type = db.Column(db.String(30), comment="权限类型")
    permission_url = db.Column(db.String(30), comment="路径地址")

    open_type = db.Column(db.String(128), comment="打开方式")
    pid = db.Column(
        db.Integer,
        db.ForeignKey("ums_permission.id"),
        default=0,
        comment="父类编号",
    )

    role_list = db.relationship(
        "RoleORM",
        secondary="ums_role_permission",
        back_populates="permission_list",
    )

    def json(self):
        return {
            "id": self.id,
            "permission_name": self.permission_name,
            "permission_code": self.permission_code,
            "permission_type": self.permission_type,
            "permission_url": self.permission_url,
            "open_type": self.open_type,
            "pid": self.pid,
        }
