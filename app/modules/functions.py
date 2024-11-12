from api.functions import (
  get_show_stories,
  get_top_stories,
  get_new_stories,
  get_best_stories
)

from utils.date_utils import (
  get_current_time,
  compare_dates
)

def get_paginated_results(query, page:int, per_page:int=15) -> tuple:
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
    article_ids = get_show_stories() + get_top_stories() + get_best_stories() + get_new_stories()

    if offset is not None:
        article_ids = article_ids[offset:]
    
    if limit is not None:
        article_ids = article_ids[:limit]

    print(len(article_ids), 'article ids found')

    # remove duplicates
    article_ids = list(set(article_ids))
    print(len(article_ids), 'unique article ids found')

    return article_ids