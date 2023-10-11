from flask_sqlalchemy import SQLAlchemy
from application import app
import os

app_path = os.path.dirname(os.path.abspath(__file__))
db_name = "articles.db"
db_path = os.path.join(app_path, db_name)
sqlite_path = 'sqlite:///' + db_path
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path

db = SQLAlchemy(app)