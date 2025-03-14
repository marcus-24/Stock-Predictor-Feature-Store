from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def correct_start_date(start_date: date, my_holidays: dict[datetime, str]) -> date:
    """If the start date is on a holiday or weekend, it is pushed
    back a day until it equals a valid trading date

    Args:
        start_date (date): original start date
        my_holidays (dict[datetime, str]): financial holdays

    Returns:
        date: corrected start date that does not land on holidays or weekends.
    """
    new_start_date = start_date  # modified date
    last_weekday_num = 4  # any weekday number greater is a weekend
    while new_start_date in my_holidays or new_start_date.weekday() > last_weekday_num:
        new_start_date = new_start_date - relativedelta(days=1)

    return new_start_date
