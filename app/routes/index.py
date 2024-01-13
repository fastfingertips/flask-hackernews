from modules.manager import (
  get_db_counts,
  get_stories
)

from flask import render_template
from cursors import app

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = get_stories(30)
    articles = sorted(articles, key=lambda x: x.score, reverse=True)

    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
    }

    return render_template('index.html', **context)