from datetime import datetime, timedelta

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