# -*- coding: utf-8 -*-

from datetime import datetime

from .string_cleanup import date_triming, duration_datetime


class Configdata:
    def __init__(self):
        self.date = None
        self.summary = ''
        self.location = ''
        self.description = ''
        self.duration = ''
        self.alarm = ''

    def diary_triming(self, *args):
        self.date, self.summary, self.description, self.duration = args
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)
        self.duration = duration_datetime(self.duration)

    def triming(self, *args):
        self.date, self.summary, self.description, self.location, self.duration, self.alarm = args
        self.alarm = 10 if self.alarm is '' else int(self.alarm)
        self.description = '스크립트에 의해 자동 생성된 이벤트입니다.' if self.description is '' else self.description
        self.date = date_triming(self.date)
        self.duration = duration_datetime(self.duration)

    @property
    def date_diaryform(self):
        return '%Y-%m-%d'

    @property
    def date_linkform(self):
        return '%Y%m%dT%H%M00'

    @property
    def date_eventform(self):
        return '%Y-%m-%dT%H:%M:00'

    def start_datetime_format(self, form):
        return datetime.strftime(self.date, form)

    def end_datetime_format(self, form):
        end_date = self.date + self.duration
        return datetime.strftime(end_date, form)
