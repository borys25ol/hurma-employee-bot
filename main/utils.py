from datetime import datetime

from main import const


def get_current_date(date_format: str = const.DEFAULT_DATE_FORMAT) -> str:
    """
    Return string with current date in based in `date_format`.
    """
    return datetime.now().strftime(date_format)
