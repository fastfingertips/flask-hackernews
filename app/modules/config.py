import os

app_root = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..'
    )
)

class DatabaseSettings:
    db_name = "articles.db"
    sqlite_uri = 'sqlite:///'

class ProjectSettings:
    @staticmethod
    def get_template_path():
        return os.path.join(app_root, 'templates')

    @staticmethod
    def get_static_path():
        return os.path.join(app_root, 'static')

class FlaskSettings:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DatabaseSettings.sqlite_uri + os.path.join(
        app_root,
        DatabaseSettings.db_name
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
