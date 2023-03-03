from typing import Optional

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from flask_sqlalchemy.pagination import Pagination
from pydantic import BaseModel, Field

from application.orms import UserORM


class QueryModel(BaseModel):
    page: int = Field(default=1)
    per_page: int = Field(default=10, ge=10, le=100)


class UserModel(QueryModel):
    mobile: str = Field(default="")


class CreateModel(QueryModel):
    nickname: str = Field(min_length=2, max_length=26)
    username: str = Field(default="")
    password: str = Field(min_length=2, max_length=26)
    mobile: str = Field(regex="^1[3456789]\d{9}$")
    email: str = Field(default="")


class EditModel(QueryModel):
    nickname: str = Field(min_length=2, max_length=26)
    username: str = Field(default="")
    mobile: str = Field(regex="^1[3456789]\d{9}$")
    email: str = Field(default="")


class UserApi(MethodView):
    # decorators = [jwt_required()]

    @validate()
    def get(self, user_id, query: UserModel):
        if user_id:
            user: UserORM = UserORM.get_by_id(user_id)
            return {
                "meta": {
                    "message": "查询用户成功",
                    "status": "success",
                },
                "result": {"user": user.json()},
            }

        filters = []
        if query.mobile:
            filters.append(UserORM.mobile.like("%" + query.mobile + "%"))

        paginate: Pagination = UserORM.query.filter(*filters).paginate(
            page=query.page, per_page=query.per_page
        )
        items: list[UserORM] = paginate.items
        return {
            "meta": {
                "message": "查询用户成功",
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
        user: UserORM = UserORM()
        user.username = body.username
        user.nickname = body.nickname
        user.password = body.password
        user.mobile = body.mobile
        user.email = body.email
        user.save_to_db()
        return {"meta": {"message": "新增用户成功", "status": "success"}}

    @validate()
    def put(self, user_id, body: EditModel):
        user: UserORM = UserORM.query.get(user_id)
        user.username = body.username
        user.nickname = body.nickname
        user.mobile = body.mobile
        user.email = body.email
        user.save_to_db()
        return {"meta": {"message": "修改用户成功", "status": "success"}}

    def delete(self, user_id):
        user: UserORM = UserORM.query.get(user_id)
        if not user:
            return {"meta": {"message": "用户不存在", "status": "fail"}}, 401
        user.delete_from_db()
        return {"meta": {"message": "删除用户成功", "status": "success"}}


def user_state_func(uid):
    user: UserORM = UserORM.query.get(uid)
    state = request.json.get("state")
    user.state = state
    user.save_to_db()

    return {
        "result": user.save_to_db(),
        "meta": {
            "message": "设置状态成功",
            "status": "success",
        },
    }
