from application.extensions import db

from .permission import PermissionORM
from .role import RoleORM
from .user import UserORM

user_role = db.Table(
    "ums_user_role",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment="标识"),
    db.Column("user_id", db.Integer, db.ForeignKey("ums_user.id"), comment="用户编号"),
    db.Column("role_id", db.Integer, db.ForeignKey("ums_role.id"), comment="角色编号"),
)

role_permission = db.Table(
    "ums_role_permission",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True, comment="标识"),
    db.Column("role_id", db.Integer, db.ForeignKey("ums_role.id"), comment="角色编号"),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("ums_permission.id"), comment="用户编号"
    ),
)
