from modules.manager import (
  get_db_counts,
)
from flask import render_template, request, redirect, url_for

from modules.models import Url
from modules.functions import get_paginated_results
from cursors import app

@app.route('/search', methods=['GET'])
def search():
    print('searching...')
    print(request.args)
    if 'q' not in request.args:
        return redirect(url_for('index'))

    query = request.args.get('q')
    formatted_query="%{}%".format(query)

    articles, pagination = get_paginated_results(
        Url.query.filter(
            Url.title.like(formatted_query) | 
            Url.url.like(formatted_query)).order_by(Url.score.desc()),
        request.args.get('page', 1, type=int)
    )

    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
        'pagination': pagination,
        'query': query
    }

    return render_template('index.html', **context)