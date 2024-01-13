from flask import (
  redirect,
  url_for,
  request
)

from cursors import (
  app,
  db
)

from modules.manager import get_story_from_db

@app.route('/favorite', methods=["GET"])
def favorite():
    referer = request.headers.get("Referer")
    story_id = request.args.get("id")

    if story_id is not None:
        article = get_story_from_db(story_id)
        if article is not None:
            article.favorite = not article.favorite
            db.session.commit()
            print(article.article_id, f'favorite: {article.favorite}')
        else:
            print('article not found in database')
    else:
        print('story_id not found')

    return redirect(referer or url_for('index'))