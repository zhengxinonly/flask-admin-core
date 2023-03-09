from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    jwt_required,
)

from application.orms import UserORM
from application.utils.response_code import RetCode

passport = Blueprint("passport", __name__)


class LoginApi(MethodView):
    def post(self):
        mobile = request.json.get("mobile")
        password = request.json.get("password")

        user: UserORM = UserORM.find_by_mobile(mobile)

        if not user:
            return {
                "meta": {
                    "code": RetCode.USER_NOTFOUND_ERR.code,
                    "status": "fail",
                    "message": RetCode.USER_NOTFOUND_ERR.msg,
                }
            }, 401
        if not user.check_password(password):
            return {
                "meta": {
                    "code": RetCode.PWD_ERR.code,
                    "status": "fail",
                    "message": RetCode.PWD_ERR.msg,
                }
            }, 401

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        return {
            "result": {
                "access_token": "Bearer " + access_token,
                "refresh_token": "Bearer " + refresh_token,
                "user_data": user.json(),
            },
            "meta": {
                "code": RetCode.OK.code,
                "status": "success",
                "message": "用户登录成功",
            },
        }


class LogoutApi(MethodView):
    decorators = [jwt_required]

    def post(self):
        return {
            "meta": {
                "code": RetCode.OK.code,
                "status": "success",
                "message": "用户退出成功",
            },
        }


@jwt_required()
def repassword_func():
    user: UserORM = current_user
    oldpassword = request.json.get("oldpassword")
    newpassword = request.json.get("newpassword")
    repassword = request.json.get("repassword")

    if not user.check_password(oldpassword):
        return {
            "meta": {
                "message": "用户密码错误",
                "status": "fail",
            },
        }, 401
    if newpassword != repassword:
        return {
            "meta": {
                "message": "两次密码不一样",
                "status": "fail",
            },
        }, 401
    user.password = newpassword
    user.save_to_db()

    return {
        "result": user.json(),
        "meta": {
            "message": "用户密码修改成功",
            "status": "success",
        },
    }
