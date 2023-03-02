from flask import Blueprint, request
from flask.views import MethodView

passport = Blueprint("passport", __name__)


class LoginApi(MethodView):
    def post(self):
        user = self.validate_login()

    @staticmethod
    def validate_login():
        username = request.json.get("username")
        password = request.json.get("password")
        return username
