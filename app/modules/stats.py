from utils.date_utils import (
  get_current_time,
  compare_dates
)

class StatsCollector:
    PERIODS = [
        ("today", 0, True),
        ("yesterday", 1, True),
        ("week", 7, False),
        ("month", 30, False),
        ("year", 365, False)
    ]

    def __init__(self, articles):
        self.articles = articles
        self.current_time = get_current_time().date()

    def _collect_period_stats(self, period_data):
        name, days, exact_match = period_data
        scores = []
        
        for article in self.articles:
            if article.visit_date is None:
                continue
                
            article_date = article.visit_date.date()
            is_in_period = compare_dates(
                article_date,
                self.current_time,
                days,
                exact_match
            )
            
            if is_in_period:
                scores.append(article.score)
        
        return scores

    def collect_stats(self):
        stats = {}
        
        for period in self.PERIODS:
            scores = self._collect_period_stats(period)
            stats[f'{period[0]}_total_visited'] = len(scores)
            stats[f'{period[0]}_total_points'] = sum(scores)
        
        return stats

def get_stats(articles):
    collector = StatsCollector(articles)
    return collector.collect_stats()