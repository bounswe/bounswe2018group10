from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import yaml
import tweepy
import os

if not os.path.isfile('.secrets.yaml'):
    raise FileExistsError('No .secrets.yaml file with the API credentials from Twitter')

application = Flask(__name__)
application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'

#TODO add author

@application.route('/')
def home():
    # check if user is authenticated
    if not is_authorized():
        return render_template('guest.html')

    # TODO: do something useful with the API
    api = get_api()
    me = api.me()

    return render_template('home.html', bag={
        'screen_name': me.screen_name,
        'name': me.name
    })


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
    application.run(debug=True)
