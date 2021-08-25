from datetime import datetime

from dateutil.relativedelta import relativedelta

from main import const


def get_current_date(
    date_format: str = const.DEFAULT_DATE_FORMAT, next_day: bool = False
) -> str:
    """
    Return string with current date in based in `date_format`.
    """
    delta = relativedelta(days=1) if next_day else relativedelta(days=0)
    date = datetime.now() + delta
    return date.strftime(date_format)
