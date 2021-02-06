from TwitterSearch import *
from datetime import date

tickers = input('Please enter the tickers you would like to see here (ex: AAPL GME TSLA) : ').split(" ")

today = date.today()

consumer_key = "joSmtoOQCwLPD9bCcaX1c4voM"
consumer_secret = "aFnZYFzf62mZG2WunjhvMDrC9LklUjNRQTE9GkT1MIPdWWdZqj"

access_token_key = "903283539860267009-8ndI3VdEEPUGO3K2uj6M8tYSWUFJRNT"
access_token_secret = "lcJd372YHdzTID26QvnqP2H1LHKkOB49ukEpEovMwbFOH"

ts = TwitterSearch(consumer_key, consumer_secret, access_token_key, access_token_secret)

try:
    for ticker in tickers:
        search_obj = TwitterSearchOrder()
        search_obj.set_keywords([ticker, '$'+ticker, ticker+'$'])
        search_obj.set_language('en')
        search_obj.set_include_entities(False)
        search_obj.set_since(today)

        count_tweets = 0
        print('checking twitter for tweets of {} ...'.format(ticker))
        for tweet in ts.search_tweets_iterable(search_obj):
            count_tweets += 1

        print('there were {} tweets of {} today'.format(count_tweets, ticker))

        search_obj.set_negative_attitude_filter()
        count_negative = 0
        for tweet in ts.search_tweets_iterable(search_obj):
            count_negative += 1

        print('according to twitter, there were {} negative tweets of {} today'.format(count_negative, ticker))

        search_obj.set_positive_attitude_filter()
        count_positive = 0
        for tweet in ts.search_tweets_iterable(search_obj):
            count_positive += 1

        print('according to twitter, there were {} positive tweets of {} today'.format(count_positive, ticker))

except TwitterSearchException as e:
    print(e)
