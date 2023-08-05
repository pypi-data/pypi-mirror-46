# -*- coding: utf-8 -*-
import re
import os
import pickle
from datetime import datetime

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from .inputconfig import date_triming
from .util import script_path


class GoogleCal:
    def __init__(self):
        self.creds = None
        self.calendar = None
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        if os.path.exists(script_path('token.pickle')):
            with open(script_path('token.pickle'), 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    script_path('credentials.json'), self.scopes)
                self.creds = flow.run_local_server()
            with open(script_path('token.pickle'), 'wb') as token:
                pickle.dump(self.creds, token)

    def build_calendar(self):
        self.calendar = build('calendar', 'v3', credentials=self.creds)
        return self.calendar

    def insert_event(self, event):
        return self.calendar.events().insert(calendarId='primary',
                                             body=event).execute()

    def quick_event(self, query):
        return self.calendar.events().quickAdd(calendarId='primary',
                                               text=query).execute()

    def calendar_list_all(self):
        page_token = None
        while True:
            events = self.calendar.events().list(calendarId='primary',
                                                 pageToken=page_token).execute()
            for event in events['items']:
                if event['status'] == 'confirmed':
                    date, = {'dateTime', 'date'}.intersection(
                        set(event['start']))
                    date_trim = re.sub(r'(.*)T(\d+):(\d+)(.*)', r'\1 \2:\3',
                                       event['start'][date])
                    element = '{:<16} {} {}'.format(date_trim, event['summary'],
                                                    event.get('reminders'))
                    print(element)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def calendar_lists(self):
        start = input('From: ')
        end = input('To: ')
        start_dt = date_triming(start)
        end_dt = date_triming(end)
        assert start_dt < end_dt, "Keep order!"

        items = list()
        page_token = None
        while True:
            events = self.calendar.events().list(calendarId='primary',
                                                 pageToken=page_token).execute()
            for event in events['items']:
                if 'dateTime' in event['start']:
                    date = datetime.strptime(event['start']['dateTime'],
                                             '%Y-%m-%dT%H:%M:%S+09:00')
                if 'date' in event['start']:
                    date = datetime.strptime(event['start']['date'], '%Y-%m-%d')
                items.append((date, EventItems(event)))
            page_token = events.get('nextPageToken')
            if not page_token:
                s = sorted(items, key=lambda t: t[0])
                for k, e in s:
                    if start_dt < k < end_dt:
                        print('{} {}'.format(
                            datetime.strftime(k, '%Y-%m-%d %H:%M'), e.summary))
                break


class EventItems:
    def __init__(self, d):
        self.__dict__ = d
