from utils.date_utils import get_current_time
from cursors import db

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, nullable=False)
    by = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer,    nullable=False)
    time = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    added_date = db.Column(db.DateTime, nullable=False, default=get_current_time())
    visited = db.Column(db.Boolean, nullable=False, default=False)
    visit_date = db.Column(db.DateTime, nullable=True, default=None)
    favorite = db.Column(db.Boolean, nullable=False, default=False)
