from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import yaml
import tweepy
import os
import json
from analysis import sentiment_analysis, get_tweet_texts

if not os.path.isfile('.secrets.yaml'):
    raise FileExistsError('No .secrets.yaml file with the API credentials from Twitter')

app = application = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def home():
    # check if user is authenticated
    if not is_authorized():
        return render_template('guest.html')

    api = get_api()
    me = api.me()

    return render_template('home.html', bag={
        'screen_name': me.screen_name,
        'name': me.name
    })


def is_authorized():
    return 'access_token' in session


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if is_authorized():
        return redirect(url_for('home'))

    tw_auth = get_auth()

    # is the user posting a PIN?
    if request.method == 'POST':
        pin_code = request.values['pin_code'].strip()
        # get permission from Twitter to access the user's account
        tw_auth.request_token = session['request_token']
        tw_auth.get_access_token(pin_code)
        # save these so we don't have to ask for it at every page refresh
        session['access_token'] = tw_auth.access_token
        session['access_token_secret'] = tw_auth.access_token_secret

        return redirect(url_for('home'))

    # guest will follow this url to authorize his account
    auth_url = tw_auth.get_authorization_url()
    # we need the request token to remember account credentials
    session['request_token'] = tw_auth.request_token

    return render_template('auth.html', auth_url=auth_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


def save_analysis_to_db(screen_name, analysis):
    if 'analysis_results' not in session:
        session['analysis_results'] = {}

    session['analysis_results'][screen_name] = analysis


def get_analysis_from_db_or_analyze(screen_name):
    saved_analysis = get_analysis_from_db(screen_name)
    if saved_analysis:
        return saved_analysis

    texts = get_tweet_texts(get_api(), screen_name)
    tweet_analysis = sentiment_analysis(texts)
    save_analysis_to_db(screen_name, tweet_analysis)
    return tweet_analysis


def get_analysis_from_db(screen_name):
    if 'analysis_results' not in session:
        return None
    if screen_name in session['analysis_results']:
        return session['analysis_results'][screen_name]
    return None


@app.route('/analysis', methods=['POST', 'GET'])
def analysis():
    if request.method == 'GET':
        return credits(url_for('home'))

    screen_name = request.values['twitter_handle'].strip().lstrip("@")
    if not screen_name:
        return redirect(url_for('home'))

    twitter_user = get_twitter_user(screen_name)
    if not twitter_user:
        return 'No such user exists'

    tweet_analysis = get_analysis_from_db_or_analyze(screen_name)
    jsoned = json.dumps(tweet_analysis)

    return render_template('analysis.html', analysis_json=jsoned, bag={
        'screen_name': twitter_user.screen_name,
        'profile_image_url': twitter_user.profile_image_url,
        'name': twitter_user.name,
        'profile_url': twitter_user.url
    })


def get_twitter_user(screen_name):
    try:
        return get_api().get_user(screen_name)
    except tweepy.error.TweepError:
        return None


def get_api():
    if 'access_token' not in session:
        raise Exception('Authorize first')

    # reconstruct auth using the values stored in the session
    auth = get_auth()
    auth.set_access_token(session['access_token'], session['access_token_secret'])
    return tweepy.API(auth)


def get_auth():
    # load credentials from secrets file to access the Twitter API
    secrets = yaml.load(open('.secrets.yaml', 'r'))
    tw_auth = tweepy.OAuthHandler(secrets['api_key'], secrets['api_secret'])
    return tw_auth


if __name__ == '__main__':
    app.run(debug=True)
