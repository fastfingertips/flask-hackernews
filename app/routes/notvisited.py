from flask import (
  render_template,
  request
)

from modules.functions import get_paginated_results
from modules.manager import get_db_counts
from modules.models import Url
from cursors import app

@app.route('/notvisited', methods=["GET"])
def notvisited():
    articles, pagination = get_paginated_results(
        Url.query.filter_by(visited=False).order_by(Url.score.desc()),
        request.args.get('page', 1, type=int)
    )

    print(f'{len(articles)} not visited articles found in database')

    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
        'pagination': pagination
    }

    return render_template('index.html', **context)