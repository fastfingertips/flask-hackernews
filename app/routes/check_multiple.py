from flask import (
  redirect,
  url_for
)

from cursors import (
  app,
  db
)

from modules.models import Url

@app.route('/check_multiple', methods=["GET"])
def check_multiple():
    articles = Url.query.all()

    for article in articles:
        if article.article_id is not None:
            articles = Url.query.filter_by(
                article_id = article.article_id
                ).all()
            if len(articles) > 1:
                print('multiple articles found in database')
                for article in articles:
                    if article.visited:
                        print(article.article_id, 'multiple visited')
                        for article in articles:
                            if not article.visited:
                                print(article.article_id, 'deleted from database')
                                db.session.delete(article)
                                db.session.commit()
                        break

    return redirect(url_for('index'))