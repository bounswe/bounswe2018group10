from flask import Flask, request, render_template, jsonify, url_for, redirect, escape
from twapi import api

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

    created = user.created_at
    created_day_of_year = created.strftime('%d %B')

    return render_template('events.html', bag={
        'is_a_user': True,
        'name': user.name,
        'screen_name': user.screen_name,
        'created_day': created_day_of_year
    })


if __name__ == '__main__':
    app.run(debug=True)
