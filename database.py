from flask_sqlalchemy import SQLAlchemy
from application import app
import os

# Define the SQLite database path
db_name = "articles.db"

# Use the 'app.root_path' to get the root directory of your Flask application
db_path = os.path.join(app.root_path, db_name)

# Configure the SQLAlchemy database URI
sqlite_uri = 'sqlite:///' + db_path
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_uri

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)