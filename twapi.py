import tweepy
import yaml

_secrets = yaml.load(open('.secrets.yaml', 'r'))


def get_api():
    oauth = tweepy.OAuthHandler(_secrets['api_key'], _secrets['api_secret'])
    oauth.set_access_token(_secrets['access_token'], _secrets['access_token_secret'])
    return tweepy.API(oauth)


api = get_api()
