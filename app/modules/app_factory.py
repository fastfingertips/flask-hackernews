from modules.config import ProjectSettings
from modules.config import FlaskSettings
from flask import Flask

def create_app():
    app = Flask(
    __name__,
    static_folder=ProjectSettings.get_static_path(),
    template_folder=ProjectSettings.get_template_path()
    )
    app.config.from_object(FlaskSettings)
    return app