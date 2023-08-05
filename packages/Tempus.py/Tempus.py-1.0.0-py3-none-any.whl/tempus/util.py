# pylint: disable=W1401

import calendar
from datetime import datetime

date_patterns = [
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%d\%m\%Y",
    "%Y\%m\%d",
]

def sign(n):
    return int(abs(n)/n) if n != 0 else 1

def is_leap_year(year):
    return year%4 == 0 and year%100 != 0 or year%400 == 0

def years_to_days(current_year, years):
    days = 0
    year = int(current_year)

    for _ in range(abs(years)):
        year += sign(years) if sign(years) < 0 else 0
        days += 366 if is_leap_year(year) else 365
        year += sign(years) if sign(years) > 0 else 0

    return days * sign(years)

def months_to_days(start_date, months, truncate=True):
    current_date = start_date
    months_count = current_date.month + abs(months)

    # Calculate the year
    year = current_date.year + int(months_count / 12)

    # Calculate the month
    month = (months_count % 12)
    if month == 0:
        month = 12

    # Calculate the day
    day = current_date.day
    last_day_of_month = calendar.monthrange(year, month)[1]

    if day > last_day_of_month:

        if truncate:
            day = last_day_of_month
        else:
            day = day - last_day_of_month
            month = month + 1

    end_date = datetime(year, month, day).date()
    difference = end_date - start_date
    difference_days = difference.days * sign(months)

    return 1 + difference_days if difference_days < 0 else difference_days

def parse_date(date_string):
    for pattern in date_patterns:
        try:
            return datetime.strptime(date_string, pattern).date()
        except ValueError:
            pass

    raise ValueError("Date is not in expected format: %s" %(date_string))
