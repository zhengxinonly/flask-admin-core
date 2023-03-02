import csv
import os

from flask import Flask, current_app

from application import db
from application.orms import PermissionORM, RoleORM, UserORM


def dict_to_orm(d, o):
    for k, v in d.items():
        setattr(o, k, v)


def csv_to_databases(path, orm):
    with open(path, encoding="utf-8") as file:
        for d in csv.DictReader(file):
            o = orm()
            dict_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()


def register_script(app: Flask):
    @app.cli.command()
    def create():
        db.drop_all()
        db.create_all()

    @app.cli.command()
    def init():
        db.drop_all()
        db.create_all()

        root = current_app.config.get("ROOT_PATH")
        user_data_path = os.path.join(root, "data", "ums_user.csv")
        csv_to_databases(user_data_path, UserORM)

        permission_data_path = os.path.join(root, "data", "ums_permission.csv")
        csv_to_databases(permission_data_path, PermissionORM)

        role_data_path = os.path.join(root, "data", "ums_role.csv")
        csv_to_databases(role_data_path, RoleORM)

        role_permission_data_path = os.path.join(
            root, "data", "ums_role_permission.csv"
        )
        with open(role_permission_data_path, encoding="utf-8") as file:
            for d in csv.DictReader(file):
                role: RoleORM = RoleORM.query.get(d["role_id"])
                permission: PermissionORM = PermissionORM.query.get(d["permission_id"])
                role.permission_list.append(permission)
                db.session.commit()

        user_role_data_path = os.path.join(root, "data", "ums_user_role.csv")
        with open(user_role_data_path, encoding="utf-8") as file:
            for d in csv.DictReader(file):
                user: UserORM = UserORM.query.get(d["user_id"])
                role: RoleORM = RoleORM.query.get(d["role_id"])
                user.role_list.append(role)
                db.session.commit()
