from database import db
import requests, time
from datetime import datetime
from tqdm import tqdm

def getCurrentTime():
    return datetime.now()

def getReq(url, timeout=5):
    while True:
        try: return requests.get(url, timeout=timeout)
        except requests.ConnectionError: # check internet connection
            print("No internet connection available.", end='\r')
            time.sleep(1)

def getTopStories():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = getReq(url)
    return r.json()

def getNewStories():
    url = 'https://hacker-news.firebaseio.com/v0/newstories.json'
    r = getReq(url)
    return r.json()

def getBestStories():
    url = 'https://hacker-news.firebaseio.com/v0/beststories.json'
    r = getReq(url)
    return r.json()

def getArticle(article_id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(article_id) + '.json'
    r = getReq(url)
    return r.json()

def articleParser(article_json):
    data = {
        'id': None,
        'by': None,
        'descendants': 0, # sometimes article has no comments
        'kids': [],
        'score': None,
        'time': None,
        'title': None,
        'type': None,
        'url': ''
    }

    for getKey, exceptValue in data.items():
        try: data[getKey] = article_json[getKey]
        except KeyError: 
            if exceptValue != None: data[getKey] = exceptValue
            else: print(f'{getKey} not found')
    return data

# -- URL --

def delete_db_blank_urls():
    from models import Url
    articles = Url.query.filter_by(url='').all()
    for article in articles:
        db.session.delete(article)
        db.session.commit()
        print(article.article_id, 'deleted')

def get_db_counts():
    from models import Url
    counts = {
        'visited': Url.query.filter_by(visited=True).count(),
        'notvisited': Url.query.filter_by(visited=False).count(),
        'favorites': Url.query.filter_by(favorite=True).count(),
    }
    return counts

def get_story_from_db(article_id):
    from models import Url
    article = Url.query.filter_by(article_id=article_id).first()
    if article is None:
        return None
    else:
        return article

def get_stories(article_limit=None, score_limit=None):
    from models import Url
    articleIds = getTopStories() + getBestStories() + getNewStories()
    print(len(articleIds), 'article ids found')
    articleIds = list(set(articleIds))
    print(len(articleIds), 'unique article ids found')
    articles = []
    already_visited_count = 0
    already_in_db_count = 0
    added_to_db_count = 0
    no_url_count = 0

    for current_article_id in tqdm(articleIds, desc='Getting stories'):
        # get article from database
        article = get_story_from_db(current_article_id)

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
                # print(rank, current_article_id, 'no url, skipping')
                no_url_count += 1
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

            # print(rank, current_article_id, 'added to database')
            added_to_db_count += 1
            
            # get article from database
            article = get_story_from_db(current_article_id)
        else:
            # print(rank, current_article_id, 'already in database')
            already_in_db_count += 1
            if article.visited:
                # print(rank, current_article_id, 'already visited')
                already_visited_count += 1
                continue

        if score_limit is not None:
            if article.score < score_limit:
                # print(current_article_id, 'score too low, skipping')
                continue

        articles.append(article)

        if article_limit is not None:
            if len(articles) >= article_limit:
                # if article limit reached, stop adding articles
                break

    data = {
        'already_in_db_count': already_in_db_count,
        'already_visited_count': already_visited_count,
        'not_visited_count': already_in_db_count - already_visited_count,
        'added_to_db_count': added_to_db_count,
        'no_url_count': no_url_count,
    }

    for k, v in data.items():
        print(k.ljust(25), v)

    return articles