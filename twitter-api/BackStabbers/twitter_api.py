import time
import yaml
import tweepy

_secrets = yaml.load(open('.secrets.yaml', 'r'))

_oauth = tweepy.OAuthHandler(_secrets['api_key'], _secrets['api_secret'])

_oauth.set_access_token(_secrets['access_token'], _secrets['access_token_secret'])


api = tweepy.API(_oauth, wait_on_rate_limit=True)


def get_friends_list(screen_name):
    friends = []
    for page in tweepy.Cursor(api.friends, screen_name=screen_name, count=200).pages():
        friends.extend([{
            "screen_name": u.screen_name,
            "name": u.name,
            "url": u.url
        } for u in page])

    return friends


def get_followers_list(screen_name):
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=screen_name, count=200).pages():
        followers.extend([{
            "screen_name": u.screen_name,
            "name": u.name,
            "url": u.url
        } for u in page])

    return followers


def get_user_details(screen_name):
    user = api.get_user(screen_name)
    if not user:
        return False

    return {
        "name": user.name,
        "screen_name": user.screen_name,
        "profile_image_url": user.profile_image_url
    }


def get_nonfollowers_list(screen_name):
    friends = get_friends_list(screen_name)
    followers = get_followers_list(screen_name)

    nonfollowers = []
    for friend in friends:
        is_friend = False
        for follower in followers:
            if friend["screen_name"] == follower["screen_name"]:
                is_friend = True

        if not is_friend:
            nonfollowers.append(friend)

    return nonfollowers
