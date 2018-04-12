from flask import Flask
import yaml
import tweepy

app = Flask(__name__)
secrets = yaml.load(open('.secrets.yaml', 'r'))


def get_api():
    oauth = tweepy.OAuthHandler(secrets['api_key'], secrets['api_secret'])
    oauth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
    return tweepy.API(oauth)


@app.route('/')
def home():
    name = get_api().me().name
    return 'Hello, {}'.format(name)


if __name__ == '__main__':
    app.run(debug=True)
