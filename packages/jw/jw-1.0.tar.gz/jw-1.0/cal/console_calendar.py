# -*- coding: utf-8 -*-
import argparse
import time
import urllib

from .googleoauth import GoogleCal
from .inputconfig import Configdata
from .util import script_path


def push_event(config):
    session = GoogleCal()
    session.build_calendar()

    event = {
        'summary': config.summary,
        'location': config.location,
        'description': config.description,
        'start': {
            'dateTime': config.start_datetime_format(config.date_eventform),
            'timeZone': 'Asia/Seoul',
        },
        'end': {
            'dateTime': config.end_datetime_format(config.date_eventform),
            'timeZone': 'Asia/Seoul',
        },
        # 'recurrence': [
        #   'RRULE:FREQ=DAILY;COUNT=' + config.duration
        # ],
        # 'attendees': [
        #   {'email': 'lpage@example.com'},
        #   {'email': 'sbrin@example.com'},
        # ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': config.alarm},
            ],
        },
    }

    session.insert_event(event)


def make_ics(config):
    uid = time.strftime('%Y-%m-%d_%H%M%S')

    ics_format = """BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:Product by Jongwon
BEGIN:VEVENT
UID:{}
DTSTART:{}
DTEND:{}
LOCATION:{}
SUMMARY:{}
DESCRIPTION:{}
BEGIN: VALARM
TRIGGER: -PT{}M
DESCRIPTION:{}
END:VALARM
END:VEVENT
END:VCALLENDAR""".format(
        uid,
        config.start_datetime_format(config.date_linkform),
        config.end_datetime_format(config.date_linkform),
        config.location,
        config.summary,
        config.description,
        config.alarm,
        config.description
    )

    # binary encoding
    ics_format = ics_format.encode('utf-8')

    # make ics
    filename = uid + '.ics'
    abs_path = script_path(filename)
    with open(abs_path, 'wb') as f:
        f.write(ics_format)

    # os.system('start ' + abspath)
    return abs_path


def google_link(config):
    uri = 'http://www.google.com/calendar/event'
    param = {
        'action': 'TEMPLATE',
        'text': config.summary,
        'dates': '/'.join([
            config.start_datetime_format(config.date_linkform),
            config.end_datetime_format(config.date_linkform)
        ]),
        'details': config.description,
        'location': config.location,
    }

    result_link = uri + '?' + urllib.parse.urlencode(param)
    return result_link


def write_diary(config):
    session = GoogleCal()
    session.build_calendar()

    event = {
        'summary': config.summary,
        'description': config.description,
        'start': {
            'date': config.start_datetime_format(config.date_diaryform)
        },
        'end': {
            'date': config.end_datetime_format(config.date_diaryform),
        }
    }
    session.insert_event(event)


def quick_init():
    query = input('Query: ')
    return query


def quick_add(query):
    session = GoogleCal()
    session.build_calendar()
    session.quick_event(query)


def call_list():
    session = GoogleCal()
    session.build_calendar()
    # session.calendar_list_all()
    session.calendar_lists()


def main_parser(kw):
    if kw.get('list'):
        call_list()
        quit()

    # Quick Add Calendar
    if kw.get('q'):
        query = quick_init()
        quick_add(query)
        print('Event created.')
        quit()

    # Initialize
    config = Configdata()

    date = input('시간: ')
    assert date is not '', '시간이 없습니다.'
    summary = input('제목: ')
    assert summary is not '', '제목이 없습니다.'
    duration = input('기간: ')
    description = input('세부정보: ')

    # Diary
    if kw.get('d'):
        config.diary_triming(date, summary, description, duration)
        write_diary(config)
        print('Event created.')
        quit()

    location = input('위치: ')
    alarm = input('알람(분 전): ')
    config.triming(date, summary, description, location, duration, alarm)

    # ICS file
    if kw.get('i'):
        abs_path = make_ics(config)
        print('ics file created at' + abs_path)

    # Google Calendar link
    if kw.get('g'):
        result_link = google_link(config)
        print('google link: ' + result_link)

    if kw.get('no_push'):
        push_event(config)
        print('Event created.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Make ics file', action='store_true')
    parser.add_argument('-d', help='Write diary', action='store_true')
    parser.add_argument('-g', help='Google calendar link', action='store_true')
    parser.add_argument('--no-push', help="Don't push my calendar",
                        action='store_false')
    parser.add_argument('-q', help='Push quickAdd calendar', action='store_true')
    parser.add_argument('-l', help='Calendar lists', action='store_true')

    args = parser.parse_args()

    main_parser(vars(args))
