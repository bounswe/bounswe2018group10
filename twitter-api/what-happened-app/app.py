from flask import Flask, request, render_template, jsonify, url_for, redirect, escape, abort
from twapi import api
from eventsapi import get_events_of_day, get_events_of_year
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/events', methods=['POST'])
def events():
    twitter_handle = request.values['twitter_handle'].strip()
    if not twitter_handle:
        return redirect(url_for('home'))

    user = api.get_user(screen_name=twitter_handle)
    if not user:
        bag = {'screen_name': twitter_handle}
        return render_template('events.html', is_a_user=False, bag=bag)

    created = user.created_at
    events_year = get_events_of_year(created.year)
    events_day = get_events_of_day(created.month, created.day)[::-1]

    bag = {
        'name': user.name,
        'screen_name': user.screen_name,
        'profile_image_url': 'https://twitter.com/{}/profile_image?size=original'.format(user.screen_name),
        'created': {
            'day': created.day,
            'month': created.strftime('%B'),
            'year': created.year
        }
    }

    return render_template('events.html', is_a_user=True, bag=bag, events_day=events_day, events_year=events_year)


@app.route('/events/<int:month>/<int:day>', methods=['GET'])
def api_events_day(month, day):
    events = get_events_of_day(month, day)

    return jsonify(events)


@app.route('/events/<int:year>', methods=['GET'])
def api_events_year(year):
    events = get_events_of_year(year)

    return jsonify(events)


@app.route('/events/<string:screen_name>')
def api_events_user(screen_name):
    user = api.get_user(screen_name=screen_name)
    if not user:
        return abort(404)

    created = user.created_at
    return jsonify({
        'created': {
            'day': created.day,
            'month': created.month,
            'year': created.year
        },
        'day': get_events_of_day(created.month, created.day),
        'year': get_events_of_year(created.year)
    })


def get_api_urls_for_day(created: datetime.datetime):
    url_day = url_for('api_events_day', month=created.month, day=created.day)
    url_year = url_for('api_events_year', year=created.year)
    return url_day, url_year


if __name__ == '__main__':
    app.run(debug=True)
