from modules.app_factory import create_app
from modules.database import SQLAlchemy

app = create_app()
db = SQLAlchemy(app)