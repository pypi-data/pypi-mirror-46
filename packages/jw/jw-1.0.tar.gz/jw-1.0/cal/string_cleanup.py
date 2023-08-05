# -*- coding: utf-8 -*-
import re
from collections import OrderedDict
from datetime import datetime, timedelta


def query_trim(patch, query, els):
    refine = re.findall(patch, query)
    assert len(refine) <= 1, 'duplicate' + patch
    return refine[0] if refine else els


def date_triming(date):
    """{'year':int, 'month':int, 'day':int, 'hour':int, 'minute':int, 'locale':string}"""
    trim_date = OrderedDict()

    # Today
    now = datetime.today()

    # parse criteria
    noon_criteria = {'오전': 'AM', '오후': 'PM', 'AM': 'AM', 'PM': 'PM'}
    nearday = {'어제': -1, '오늘': 0, '내일': 1, '모레': 2}

    # ex) 내일 오후 3시 = 2017년 5월 17일 3시 0분 PM
    trim_date['year'] = format(query_trim(r'(\d+)년', date, now.year))
    trim_date['month'] = format(query_trim(r'(\d+)월', date, now.month))
    trim_date['day'] = format(query_trim(r'(\d+)일', date, now.day))

    # default time 7:00 AM
    trim_date['hour'] = format(query_trim(r'(\d+)시', date, 7))
    trim_date['minute'] = format(query_trim(r'(\d+)분', date, 0))

    trim_date['locale'] = noon_criteria[query_trim(r'(오전|오후|AM|PM)', date, 'AM')]

    # make datetime
    start_date = datetime.strptime('/'.join(trim_date.values()), '/'.join(
        ['%Y', '%m', '%d', '%I', '%M', '%p']))

    near_days = nearday[query_trim(r'(어제|오늘|내일|모레)', date, '오늘')]
    near_delta = timedelta(days=near_days)

    return start_date + near_delta


def duration_datetime(date):
    day = int(query_trim(r'(\d+)일', date, 1)) - 1
    hour = int(query_trim(r'(\d+)시', date, 1))
    minute = int(query_trim(r'(\d+)분', date, 0))

    return timedelta(days=day, hours=hour, minutes=minute)
