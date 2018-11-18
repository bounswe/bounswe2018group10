from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from info import data
import json

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# listener that handles streaming data
class listener(StreamListener):
    def on_connect(self):
        print('Stream starting...')

    def on_status(self, status):
        if status.geo is not None:
            t = dict()
            t['text'] = status.text
            t['coordinates'] = status.coordinates
            data.append(t)

    def on_error(self, status):
        print(status)


def main():
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=[
        -180.0, -90.0, 180.0, 90.0
    ])
