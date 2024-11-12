from flask import (
  redirect,
  request,
  url_for
)

from cursors import (
  app,
  db
)

from utils.date_utils import get_current_time
from modules.manager import get_story_from_db

@app.route('/visit', methods=["GET"])
def visit():
    referer = request.headers.get("Referer")
    story_id = request.args.get("id")

    if story_id is not None:
        article = get_story_from_db(story_id)
        if article is not None:
            if not article.visited:
                article.visited = True
                article.visit_date = get_current_time()
                db.session.commit()
                print(article.article_id, 'marked as visited')
                return redirect(article.url)
            else:
                print(article.article_id, 'already visited')
        else:
            print('article not found in database')
    else:
        print('story_id not found')

    return redirect(referer or url_for('index'))