# date-time parsing function for loading the dataset
from pandas import datetime


class DateParser(object):
    def parse(self, date):
        return datetime.strptime('190' + date, '%Y-%m')
