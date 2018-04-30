# -*- coding: utf-8 -*-

# author: Baran Kılıç

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_restful import Resource, Api
import yaml
import tweepy
import os

if not os.path.isfile('.secrets.yaml'):
    raise FileExistsError('No .secrets.yaml file with the API credentials from Twitter')

application = Flask(__name__)
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'

flask_restful_api = Api(application)

class SearchJobApi(Resource):
    def get(self,skill):
        api = get_api()
        query = skill + ' AND (JOB OR JOBS OR CAREER OR CAREERS OR HIRE OR HIRING OR RECRUIT OR RECRUITING OR ' \
                           'EMPLOY OR EMPLOYING OR EMPLOYMENT OR CV OR OPPORTUNITY OR OPPORTUNITIES OR ROLE OR ROLES OR ' \
                           'POSITION OR SKILLED OR CONTRACT OR SALARY)'
        max_tweets = 20
        searchResult = tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(max_tweets)

        dict = {}
        dict['tweets'] = []
        for tweet in searchResult:
            t = {}
            t['author'] = {}
            t['author']['name'] = tweet.author.name
            t['author']['screen_name'] = tweet.author.screen_name
            t['author']['profile_image_url'] = tweet.author.profile_image_url
            t['text'] = tweet.full_text
            t['created_at'] = tweet.created_at
            t['id_str'] = tweet.id_str
            dict['tweets'].append(t)
        return jsonify(dict)


class FollowApi(Resource):
    def get(self,screen_name):
        api = get_api()
        api.create_friendship(screen_name=screen_name, follow=True)
        return jsonify({'message': 'You are now following '+screen_name})


flask_restful_api.add_resource(SearchJobApi, '/api/search/<string:skill>')
flask_restful_api.add_resource(FollowApi, '/api/follow/<string:screen_name>')


@application.route('/')
def home():
    # check if user is authenticated
    if not is_authorized():
        return render_template('guest.html')

    api = get_api()
    me = api.me()

    quick_link_list = ['python', 'java', 'javascript', 'php', 'nodejs', 'cpp', 'swift']

    tips = ['"Your profile is your brand. Better add a profile picture and bio to your profile!"',
            '"Follow the companies and recruiters you are interested in!"',
            '"Start a Twitter conversation!"',
            '"Be someone worth following!"']

    return render_template('home.html', bag={
        'screen_name': me.screen_name,
        'name': me.name
    }, quick_link_list=quick_link_list, tips=tips)


@application.route('/follow/<user_id>/<screen_name>')
def follow_user(user_id, screen_name):
    api = get_api()
    api.create_friendship(user_id=user_id, follow=True)
    return render_template('follow.html', screen_name=screen_name)


@application.route('/search_job', methods=['POST'])
def search_job():
    api = get_api()
    job_name = request.values['job'].strip()
    query = job_name + ' AND (JOB OR JOBS OR CAREER OR CAREERS OR HIRE OR HIRING OR RECRUIT OR RECRUITING OR ' \
                       'EMPLOY OR EMPLOYING OR EMPLOYMENT OR CV OR OPPORTUNITY OR OPPORTUNITIES OR ROLE OR ROLES OR ' \
                       'POSITION OR SKILLED OR CONTRACT OR SALARY)'
    max_tweets = 20
    # lang='en' ,include_entities=True  result_type='popular'
    searchResult = tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(max_tweets)
    # searchResult = api.search(q=query, lang='en',include_entities=True)
    return render_template('search_job.html', searchResult=searchResult)


def is_authorized():
    return 'access_token' in session


@application.route('/auth', methods=['GET', 'POST'])
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


@application.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


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
    tw_auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
    return tw_auth


if __name__ == '__main__':
    # TODO: turn off debugging on production
    application.run(debug=False)
