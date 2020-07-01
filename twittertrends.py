from tweepy import OAuthHandler
from tweepy import API
from config import twitter_credentials
import datetime
import DB_writer


def get_trends():
    # Consumer key authentication(consumer_key,consumer_secret can be collected from our twitter developer profile)
    auth = OAuthHandler(twitter_credentials['api_key'], twitter_credentials['api_secret_key'])

    # Access key authentication(access_token,access_token_secret can be collected from our twitter developer profile)
    auth.set_access_token(twitter_credentials['access_token'], twitter_credentials['access_token_secret'])

    # Set up the API with the authentication handler
    api = API(auth)

    # Germany WOEID
    woeid = 23424829

    # Get trends
    trends = api.trends_place(woeid)
    trends = trends[0]['trends']
    now = datetime.datetime.now()
    trends = [{"keyword": t['name'], "volume": t['tweet_volume'], "tmstmp": now} for t in trends]

    for t in trends:
        DB_writer.insert_trends(t)