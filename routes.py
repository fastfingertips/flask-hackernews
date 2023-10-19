from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from functions import (
    get_db_counts,
    get_current_time,
    get_story_from_db,
    get_stories,
    get_stats
)

from application import app
from database import db
from models import Url

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = get_stories(30)

    articles_sorted = sorted(articles, key=lambda x: x.score, reverse=True)
    context = {
        'counts': get_db_counts(),
        'articles': articles_sorted,
        'theme': 'dark',
    }

    return render_template('index.html', **context)

@app.route('/visited', methods=["GET"])
def visited():
    articles = Url.query.filter_by(visited=True).all()
    articles = articles[::-1] # reverse order
    print(len(articles), 'visited articles found in database')
    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
    }

    return render_template('index.html', **context)

@app.route('/notvisited', methods=["GET"])
def notvisited():
    articles = Url.query.filter_by(visited=False).all()
    articles = sorted(articles, key=lambda x: x.score, reverse=True)
    articles_top = articles[:30]
    print(len(articles), 'not visited articles found in database')
    context = {
        'counts': get_db_counts(),
        'articles': articles_top,
        'theme': 'dark',
    }
    return render_template('index.html', **context)

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

@app.route('/favorites', methods=["GET"])
def favorites():
    articles = Url.query.filter_by(favorite=True).all()
    articles = articles[::-1] # reverse order for latest first
    print(len(articles), 'favorite articles found in database')
    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
    }
    return render_template('favorites.html', **context)

# -- INIT ROUTES --

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
            else: print(article.article_id, 'already visited')
        else: print('article not found in database')
    else: print('story_id not found')

    return redirect(referer or url_for('index'))

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
        else: print('article not found in database')
    else: print('story_id not found')

    return redirect(referer or url_for('index'))

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