from flask import render_template
from modules.manager import get_db_counts
from modules.functions import get_stats
from modules.models import Url
from cursors import app

@app.route('/stats', methods=["GET"])
def stats():
    all_articles = Url.query.filter_by(visited=True).all()
    stats = get_stats(all_articles)

    context = {
    'counts': get_db_counts(),
    'theme': 'dark'
    }

    context.update(stats)
    return render_template('stats.html', **context)