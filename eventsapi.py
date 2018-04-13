import requests
import json
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup as soupify


def _get_soup(url):
    html = urlopen(url)
    return soupify(html, 'html.parser')


def get_events_of_day(month, day):
    endpoint = "https://onthisday.salatart.com/api/episodes?day={}&month={}".format(day, month)
    raw_events = json.loads(requests.get(endpoint).text)

    events = []
    for ev in raw_events['events']:
        events.append({
            'year': ev['year'],
            'event': ev['data']
        })

    return events


def _clean_soup(node):
    [sup.extract() for sup in node.find_all('sup')]
    [edit.extract() for edit in node.find_all('span', {'class': 'mw-editsection'})]
    return node


def _parse_event(raw):
    parts = raw.rsplit(' – ', 1)
    if len(parts) < 2:
        parts = raw.rsplit(' - ', 1)
    return {
        'day': parts[0],
        'event': parts[1]
    }


def _parse_multiple_events(raw):
    lines = [line for line in raw.strip().split('\n') if line is not ""]
    day = lines.pop(0)
    return [{
        'day': day,
        'event': event
    } for event in lines]


def get_events_year(year):
    endpoint = "https://en.wikipedia.org/wiki/{}".format(year)
    soup = _get_soup(endpoint)
    soup.find('h2', text='Events')

    # the titles for respective sections
    starting_point = [h2 for h2 in soup.find_all('h2') if re.match('^Events', h2.text)][0]
    ending_point = [h2 for h2 in soup.find_all('h2') if re.match('^Births', h2.text)][0]

    # the list of months coming after these points
    lists_after_start = list(starting_point.find_next_siblings('ul'))
    lists_after_end = list(ending_point.find_next_siblings('ul'))

    monthly_events = []
    for ev in lists_after_start:
        if ev not in lists_after_end:
            monthly_events.append(ev)

    events = []
    for month in monthly_events:
        _clean_soup(month)
        monthly = {
            'month': _clean_soup(month.find_previous('h3')).text.strip(),
            'events': []
        }
        for ev in month.find_all('li', recursive=False):
            if ev.find('ul'):
                monthly['events'].extend(_parse_multiple_events(ev.text))
            else:
                monthly['events'].append(_parse_event(ev.text))

        events.append(monthly)

    return events
