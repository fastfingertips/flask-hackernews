from .client import get_hn_item, get_stories_by_type

def get_show_stories():
    return get_stories_by_type('show')

def get_top_stories():
    return get_stories_by_type('top')

def get_new_stories():
    return get_stories_by_type('new')

def get_best_stories():
    return get_stories_by_type('best')

def get_article(article_id):
    return get_hn_item(article_id)

def get_story_from_id(story_id):
    return get_hn_item(story_id)

def get_comment_from_id(comment_id):
    return get_hn_item(comment_id)

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