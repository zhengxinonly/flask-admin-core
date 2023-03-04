from flask import Blueprint, Flask

from application.api.passport import LoginApi, LogoutApi
from application.api.rights import RightsAPI
from application.api.roles import RoleAPI
from application.api.users import UserApi, user_state_func
from application.utils.functools import register_rest_api


def register_api(app: Flask):
    api = Blueprint("api", __name__, url_prefix="/api/v1")

    api.add_url_rule(
        "/login", view_func=LoginApi.as_view("login_api"), methods=["POST"]
    )
    api.add_url_rule(
        "/logout", view_func=LogoutApi.as_view("logout_api"), methods=["POST"]
    )

    register_rest_api(api, UserApi, "user_api", "/user/", pk="user_id")

    api.add_url_rule(
        "/user/<int:uid>/state", view_func=user_state_func, methods=["PUT"]
    )

    register_rest_api(api, RightsAPI, "rights_api", "/rights/", pk="rights_id")

    register_rest_api(api, RoleAPI, "role_api", "/role/", pk="role_id")

    app.register_blueprint(api)
