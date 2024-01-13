from cursors import (
    app,
    db
)

import routes

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()