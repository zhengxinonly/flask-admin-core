from typing import Optional

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from flask_sqlalchemy.pagination import Pagination
from pydantic import BaseModel, Field

from application.orms import PermissionORM


class QueryModel(BaseModel):
    page: int = Field(default=1)
    per_page: int = Field(default=10, ge=10, le=100)


class RightsModel(QueryModel):
    permission_name: str = Field(default="")


class RightsAPI(MethodView):
    @validate()
    def get(self, rights_id, query: RightsModel):
        if rights_id:
            rights: PermissionORM = PermissionORM.query.get(rights_id)
            return {
                "meta": {
                    "message": "查询权限成功",
                    "status": "success",
                },
                "result": {"rights": rights.json()},
            }
        filters = []
        if query.permission_name:
            filters.append(
                PermissionORM.permission_name.like("%" + query.permission_name + "%")
            )

        paginate: Pagination = PermissionORM.query.filter(*filters).paginate(
            page=query.page, per_page=query.per_page
        )
        items: list[PermissionORM] = paginate.items
        return {
            "meta": {
                "message": "查询权限成功",
                "status": "success",
            },
            "result": {
                "total": paginate.total,
                "page": paginate.page,
                "pre_page": paginate.per_page,
                "users": [item.json() for item in items],
            },
        }

    def post(self):
        return {
            "meta": {
                "message": "暂未实现新增权限功能",
                "status": "success",
            },
            "result": None,
        }

    def put(self, rights_id):
        return {
            "meta": {
                "message": "暂未实现修改权限功能",
                "status": "success",
            },
            "result": None,
        }

    def delete(self, rights_id):
        return {
            "meta": {
                "message": "暂未实现删除权限功能",
                "status": "success",
            },
            "result": None,
        }
