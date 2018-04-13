from flask import Flask, request, render_template, jsonify, url_for, redirect, escape
from twapi import api
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
        return render_template('events.html', bag={
            'is_a_user': False,
            'screen_name': twitter_handle
        })

    created: datetime.datetime = user.created_at

    (url_day, url_year) = get_api_urls_for_day(created)
    return render_template('events.html', bag={
        'is_a_user': True,
        'name': user.name,
        'screen_name': user.screen_name,
        'created': {
            'day': created.day,
            'month': created.strftime('%B'),
            'year': created.year,
            'url_day': url_day,
            'url_year': url_year
        }
    })


@app.route('/events/<int:month>/<int:day>', methods=['GET'])
def api_events_day(month, day):
    return "{}".format(month)


@app.route('/events/<int:year>', methods=['GET'])
def api_events_year(year):
    return "{}".format(year)


def get_api_urls_for_day(created: datetime.datetime):
    url_day = url_for('api_events_day', month=created.month, day=created.day)
    url_year = url_for('api_events_year', year=created.year)
    return url_day, url_year


if __name__ == '__main__':
    app.run(debug=True)
