from flask import Flask

import application.orms
from application.api import register_api
from application.extensions import db, register_extension
from application.extensions.init_script import register_script
from config import config_dict


def create_app(cfg_name="dev"):
    app = Flask("application")
    config_object = config_dict[cfg_name]
    app.config.from_object(config_object)

    register_extension(app)
    register_api(app)

    if app.config.get("CONFIG_NAME") == "dev":
        register_script(app)
    return app
