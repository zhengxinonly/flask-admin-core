from flask import Flask

from application.extensions import register_extension
from config import config_dict


def create_app(cfg_name="dev"):
    app = Flask("application")
    config_object = config_dict[cfg_name]
    app.config.from_object(config_object)

    register_extension(app)
    return app
