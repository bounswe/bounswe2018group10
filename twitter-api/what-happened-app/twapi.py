import tweepy
import yaml
import os

if 'TWITTER_API_KEY' in os.environ:
    _secrets = {
        'api_key': os.environ['TWITTER_API_KEY'],
        'api_secret': os.environ['TWITTER_API_SECRET'],
        'access_token': os.environ['TWITTER_ACCESS_TOKEN'],
        'access_token_secret': os.environ['TWITTER_ACCESS_SECRET']
    }
elif os.path.isfile('.secrets.yaml'):
    _secrets = yaml.load(open('.secrets.yaml', 'r'))
else:
    raise SystemError('No API credentials given')


def get_api():
    oauth = tweepy.OAuthHandler(_secrets['api_key'], _secrets['api_secret'])
    oauth.set_access_token(_secrets['access_token'], _secrets['access_token_secret'])
    return tweepy.API(oauth)


api = get_api()
cursor = tweepy.Cursor
