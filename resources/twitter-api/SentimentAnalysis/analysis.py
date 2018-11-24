from textblob import TextBlob as analyze
import tweepy


def percentage(part, whole):
    if whole != 0:
        return 100 * float(part) / float(whole)
    else:
        return 0


def sentiment_analysis(texts):
    positive = 0
    negative = 0
    neutral = 0
    counter = 0
    subjectivity = 0

    for text in texts:
        counter += 1
        analysis = analyze(text)
        subjectivity += analysis.sentiment.subjectivity
        curr_polarity = analysis.sentiment.polarity
        if curr_polarity >= 0.05:
            positive += 1
        elif 0.05 > curr_polarity > -0.05:
            neutral += 1
        elif curr_polarity <= -0.05:
            negative += 1

    positive = percentage(positive, counter)
    negative = percentage(negative, counter)
    neutral = percentage(neutral, counter)
    subjectivity = percentage(subjectivity, counter)

    return {
        'positive': positive,
        'negative': negative,
        'neutral': neutral,
        'subjectivity': subjectivity
    }


def get_tweet_texts(api, username):
    tweets = []
    for tw in tweepy.Cursor(api.user_timeline, screen_name=username).items(100):
        tweets.append(tw.text)

    return tweets
