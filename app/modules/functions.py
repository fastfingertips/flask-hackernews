from api.functions import (
  get_show_stories,
  get_top_stories,
  get_new_stories,
  get_best_stories
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