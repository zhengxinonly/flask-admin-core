from typing import Optional

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from flask_sqlalchemy.pagination import Pagination
from pydantic import BaseModel, Field

from application.orms import RoleORM


class QueryModel(BaseModel):
    page: int = Field(default=1)
    per_page: int = Field(default=10, ge=10, le=100)


class UserModel(QueryModel):
    name: str = Field(default="")


class CreateModel(QueryModel):
    name: str
    code: str
    desc: str = Field(default="")


class RoleAPI(MethodView):
    # decorators = [jwt_required()]

    @validate()
    def get(self, role_id, query: UserModel):
        if role_id:
            role: RoleORM = RoleORM.query.get(role_id)
            return {
                "meta": {
                    "message": "查询用户成功",
                    "status": "success",
                },
                "result": {"user": role.json()},
            }

        filters = []
        if query.name:
            filters.append(RoleORM.name.like("%" + query.name + "%"))

        paginate: Pagination = RoleORM.query.filter(*filters).paginate(
            page=query.page, per_page=query.per_page
        )
        items: list[RoleORM] = paginate.items
        return {
            "meta": {
                "message": "查询角色成功",
                "status": "success",
            },
            "result": {
                "total": paginate.total,
                "page": paginate.page,
                "pre_page": paginate.per_page,
                "users": [item.json() for item in items],
            },
        }

    @validate()
    def post(self, body: CreateModel):
        role: RoleORM = RoleORM()
        role.name = body.name
        role.code = body.code
        role.desc = body.desc

        role.save_to_db()
        return {
            "meta": {
                "message": "新增角色成功",
                "status": "success",
            },
        }

    @validate()
    def put(self, role_id, body: CreateModel):
        role: RoleORM = RoleORM.query.get(role_id)
        role.name = body.name
        role.code = body.code
        role.desc = body.desc
        role.save_to_db()
        return {
            "meta": {
                "message": "修改角色成功",
                "status": "success",
            },
        }

    def delete(self, role_id):
        role: RoleORM = RoleORM.query.get(role_id)
        if not role:
            return {"meta": {"message": "角色不存在", "status": "fail"}}, 401
        role.delete_from_db()
        return {
            "meta": {
                "message": "删除角色成功",
                "status": "success",
            },
        }
