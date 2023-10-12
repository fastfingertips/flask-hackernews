from database import db
import requests, time
from datetime import datetime

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