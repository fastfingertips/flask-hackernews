from tqdm import tqdm
from modules.functions import get_story_ids
from modules.models import Url
from cursors import db
from api.functions import (
  article_parser,
  get_article
)

def get_stories(article_limit:int=30, score_limit:int=0, offset=None):
    article_ids = get_story_ids(offset=offset, limit=None)
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

        if article.score < score_limit:
            # print(current_article_id, 'score too low, skipping')
            continue

        articles.append(article)

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

def get_story_from_db(article_id):
    article = Url.query.filter_by(article_id=article_id).first()
    if article is None:
        return None
    else:
        return article
    
def delete_db_blank_urls():
  articles = Url.query.filter_by(url='').all()
  for article in articles:
      db.session.delete(article)
      db.session.commit()
      print(article.article_id, 'deleted')

def get_db_counts():
    counts = {
        'visited': Url.query.filter_by(visited=True).count(),
        'notvisited': Url.query.filter_by(visited=False).count(),
        'favorites': Url.query.filter_by(favorite=True).count(),
        'total': Url.query.count(),
    }
    return counts
