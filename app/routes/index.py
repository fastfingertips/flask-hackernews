from modules.manager import (
  get_db_counts,
  get_stories
)

from flask import render_template, request
from cursors import app

@app.route('/', methods=['GET', 'POST'])
def index():

    articles = get_stories(
        request.args.get('limit', 30, type=int),
        request.args.get('min', 0, type=int)
        )

    articles = sorted(articles, key=lambda x: x.score, reverse=True)

    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
    }

    return render_template('index.html', **context)