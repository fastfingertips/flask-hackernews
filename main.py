from application import app
from database import db
from routes import (
  index,
  visit,
  visited,
  favorite,
  favorites
)

# print(app.url_map)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)