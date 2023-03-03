from typing import Optional

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from flask_sqlalchemy.pagination import Pagination
from pydantic import BaseModel, Field

from application.orms import UserORM


class RightsAPI(MethodView):
    def get(self, rights_id):
        if rights_id:
            pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
