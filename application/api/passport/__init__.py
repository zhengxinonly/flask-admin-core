from flask import Blueprint, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

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
                "refresh_token": refresh_token,
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
