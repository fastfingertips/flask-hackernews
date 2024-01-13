from datetime import (
  datetime,
  timedelta
)

import requests
import time

def get_paginated_results(query, page:int, per_page:int=30) -> tuple:
    offset = (page - 1) * per_page
    """
    offset: The number of rows to skip, starting from the first row.
    limit: The maximum number of rows to be returned, starting from the offset row.
    all: Return the results as a list.
    https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.offset
    https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.limit
    https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.all

    https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/api/#module-flask_sqlalchemy.pagination
    https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/api/#flask_sqlalchemy.SQLAlchemy.paginate
    """
    results = query.offset(offset).limit(per_page).all()
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return results, pagination

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
            if exceptValue is not None: data[getKey] = exceptValue
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

def get_story_ids(offset=None, limit=None):
    # get article ids from api
    article_ids = get_top_stories() + get_best_stories() + get_new_stories()

    if offset is not None:
        article_ids = article_ids[offset:]
    
    if limit is not None:
        article_ids = article_ids[:limit]

    print(len(article_ids), 'article ids found')

    # remove duplicates
    article_ids = list(set(article_ids))
    print(len(article_ids), 'unique article ids found')

    return article_ids

