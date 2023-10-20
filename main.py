from application import app
from database import db
from routes import (
  index,
  visit,
  visited,
  favorite,
  favorites
)

from config import Config

# Configure the application using the "Config" class
app.config.from_object(Config)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()