from database import db
import requests, time
from datetime import datetime, timedelta
from tqdm import tqdm

def get_current_time():
    return datetime.now()

def compare_dates(date_1, date_2, days=0, focus=True):
    """
    Compare two dates and determine if they are equal or one is greater than the other.

    Args:
    - date_1 (datetime): The first date to compare.
    - date_2 (datetime): The second date to compare.
    - days (int): Number of days to subtract from date_2 for comparison.
                   Defaults to 0.
    - focus (bool): If True, check for equality; if False, check for greater than or equal.
                    Defaults to True.

    Returns:
    - bool: True if the condition is met, otherwise False.
    """
    past_date = date_2 - timedelta(days=days)
    if focus:
        return date_1 == past_date
    return date_1 >= past_date

def get_req(url, timeout=5):
    while True:
        try: return requests.get(url, timeout=timeout)
        except requests.ConnectionError: # check internet connection
            print("No internet connection available.", end='\r')
            time.sleep(1)

def get_top_stories():
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = get_req(url)
    return r.json()

def get_new_stories():
    url = 'https://hacker-news.firebaseio.com/v0/newstories.json'
    r = get_req(url)
    return r.json()

def get_best_stories():
    url = 'https://hacker-news.firebaseio.com/v0/beststories.json'
    r = get_req(url)
    return r.json()

def get_article(article_id):
    url = f'https://hacker-news.firebaseio.com/v0/item/{article_id}.json'
    r = get_req(url)
    return r.json()

def article_parser(article_json):
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

def get_stats(articles):
    today_visited_scores = []
    yesterday_visited_scores = []
    week_visited_scores = []
    month_visited_scores = []
    year_visited_scores = []

    for article in articles:
        if article.visit_date is not None:
            article_date = article.visit_date.date()
            current_time = get_current_time().date()
            if compare_dates(article_date, current_time):
                today_visited_scores.append(article.score)
            if compare_dates(article_date, current_time, 1):
                yesterday_visited_scores.append(article.score)
            if compare_dates(article_date, current_time, 7, False):
                week_visited_scores.append(article.score)
            if compare_dates(article_date, current_time, 30, False):
                month_visited_scores.append(article.score)
            if compare_dates(article_date, current_time, 365, False):
                year_visited_scores.append(article.score)

    context = {
        'today_total_visited': len(today_visited_scores),
        'today_total_points': sum(today_visited_scores),
        'yesterday_total_visited': len(yesterday_visited_scores),
        'yesterday_total_points': sum(yesterday_visited_scores),
        'week_total_visited': len(week_visited_scores),
        'week_total_points': sum(week_visited_scores),
        'month_total_visited': len(month_visited_scores),
        'month_total_points': sum(month_visited_scores),
        'year_total_visited': len(year_visited_scores),
        'year_total_points': sum(year_visited_scores),
    }

    return context

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
        'total': Url.query.count(),
    }
    return counts

def get_story_from_db(article_id):
    from models import Url
    article = Url.query.filter_by(article_id=article_id).first()
    if article is None:
        return None
    else:
        return article

def get_story_ids():
    # get article ids from api
    article_ids = get_top_stories() + get_best_stories() + get_new_stories()
    print(len(article_ids), 'article ids found')

    # remove duplicates
    article_ids = list(set(article_ids))
    print(len(article_ids), 'unique article ids found')

    return article_ids

def get_stories(article_limit=None, score_limit=None):
    from models import Url
    article_ids = get_story_ids()
    articles = []
    already_visited_count = 0
    already_in_db_count = 0
    added_to_db_count = 0
    no_url_count = 0

    for current_article_id in tqdm(article_ids, desc='Getting stories'):
        # get article from database
        article = get_story_from_db(current_article_id)

        # check if article is already in database
        if article is None:

            # get article from api
            articleJson = get_article(current_article_id)
            articleDict = article_parser(articleJson)

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