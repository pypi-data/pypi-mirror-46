import locale
from datetime import datetime, timedelta
from tempus.util import parse_date, years_to_days, months_to_days

class Tempus:
    def __init__(self, date=None, flag=True):
        self.date = self.now()
        self.flag = flag

        if date:
            self.date = parse_date(date)

    def now(self):
        return datetime.now().date()

    def today(self):
        return self.now()

    def tomorrow(self):
        return self.now() + timedelta(days=1)

    def yesterday(self):
        return self.now() - timedelta(days=1)

    def get(self):
        return self.date

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    @property
    def day(self):
        return self.date.day

    @property
    def weekday(self):
        return self.date.weekday()

    @property
    def weekday_name(self):
        return self.date.strftime('%A').lower()

    @property
    def weekday_name_abbr(self):
        return self.date.strftime('%a').lower()

    @property
    def month_name(self):
        return self.date.strftime('%B').lower()

    @property
    def month_name_abbr(self):
        return self.date.strftime('%b').lower()

    def setFlag(self, flag):
        self.flag = flag
        return self

    def locale(self, arg):
        locale.setlocale(locale.LC_ALL, arg)
        return self

    def add(self, **kwds):
        units = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds', 'microseconds']

        for key, value in kwds.items():
            if key in units:

                if key == 'years':
                    key = 'days'
                    value = years_to_days(self.date.year, value)

                if key == 'months':
                    key = 'days'
                    value = months_to_days(self.date, value, self.flag)

                self.date = self.date + timedelta(**{key: value})
        return self

    def substract(self, **kwds):
        for value in kwds:
            kwds[value] = kwds[value] * -1
        return self.add(**kwds)
