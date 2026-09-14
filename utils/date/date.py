import time
from datetime import datetime
import pytz


class DateHelper:

    def __init__(self, timestamp, _format='%d.%m.%Y %H:%M:%S'):
        self.format = _format
        self.timezone = pytz.timezone('Europe/Moscow')
        self.datetime = datetime.fromtimestamp(timestamp)
        self.utctime = pytz.utc.localize(self.datetime)

    def get_date(self):
        return self.utctime.strftime(self.format)

    def get_now(self):
        now = datetime.fromtimestamp(time.time())
        utctime = pytz.utc.localize(now)
        return utctime.strftime(self.format)
