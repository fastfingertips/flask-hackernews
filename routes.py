from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from functions import (
    getTopStories,
    getNewStories,
    getBestStories,
    get_db_counts,
    getArticle,
    articleParser,
    getCurrentTime
)

from application import app
from database import db
from models import Url

@app.route('/', methods=['GET', 'POST'])
def index():
    article_limit = 30
    score_limit = 0
    articleIds = getTopStories() + getBestStories() # + getNewStories()
    print(len(articleIds), 'article ids found')
    articleIds = list(set(articleIds))
    print(len(articleIds), 'unique article ids found')
    articles = []

    visited_count = Url.query.filter_by(visited=True).count()
    print(f'visited count: {visited_count}')

    for rank, current_article_id in enumerate(articleIds):
        # get article from database
        article = Url.query.filter_by(
            article_id=current_article_id
            ).first()

        # check if article is already in database
        if article is None:

            # get article from api
            articleJson = getArticle(current_article_id)
            articleDict = articleParser(articleJson)

            # if url is not valid, skip article
            if articleDict['url'] == '':
                """
                Already in database, but url is empty
                DELETE FROM url WHERE url = ''
                SELECT * FROM url WHERE url = ''
                """
                print(rank, current_article_id, 'no url, skipping')
                continue

            new_article = Url(
                article_id = articleDict['id'],
                by=articleDict['by'],
                score=articleDict['score'],
                time=articleDict['time'],
                title=articleDict['title'],
                url=articleDict['url'],
            )

            db.session.add(new_article)
            db.session.commit()

            print(rank, current_article_id, 'added to database')
            
            # get article from database
            article = Url.query.filter_by(
                article_id=current_article_id
                ).first()
        else:
            print(rank, current_article_id, 'already in database')
            if article.visited:
                print(rank, current_article_id, 'already visited')
                continue

        """
        if article.score < score_limit:
            print(rank, current_article_id, 'score too low, skipping')
            continue
        """

        articles.append(article)
                
        if len(articles) >= article_limit:
            # if article limit reached, stop adding articles
            break

    articles_sorted = sorted(articles, key=lambda x: x.score, reverse=True)
    context = {
        'counts': get_db_counts(),
        'articles': articles_sorted,
        'theme': 'dark',
    }

    print(len(articles), 'articles added to context')
    
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
    print(len(articles), 'not visited articles found in database')
    context = {
        'counts': get_db_counts(),
        'articles': articles,
        'theme': 'dark',
    }
    return render_template('index.html', **context)

@app.route('/favorites', methods=["GET"])
def favorites():
    articles = Url.query.filter_by(favorite=True).all()
    articles = articles[::-1] # reverse order
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
    _id = request.args.get("id")

    article = Url.query.filter_by(article_id=_id).first()

    if article is not None:
        if not article.visited:
            article.visited = True
            article.visit_date = getCurrentTime()
            db.session.commit()
            print(article.article_id, 'marked as visited')
            return redirect(article.url)
        else: print(article.article_id, 'already visited')
    else: print('article not found in database')

    return redirect(referer or url_for('index'))

@app.route('/favorite', methods=["GET"])
def favorite():
    referer = request.headers.get("Referer")
    _id = request.args.get("id")
    article = Url.query.filter_by(article_id=_id).first()
    if article is not None:
        article.favorite = not article.favorite
        db.session.commit()
        print(article.article_id, f'favorite: {article.favorite}')
    else: print('article not found in database')
    return redirect(referer or url_for('index'))