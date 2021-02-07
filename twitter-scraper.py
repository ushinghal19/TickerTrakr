from flask import Flask, redirect, url_for, render_template, request
from TwitterSearch import *
from datetime import date, timedelta

import praw
from reddit_stocks import search_ticker_mentions, search_ticker_upvotes

app = Flask(__name__)

today = date.today()
yesterday = today - timedelta(1)

CONSUMER_KEY = "joSmtoOQCwLPD9bCcaX1c4voM"
CONSUMER_SECRET = "aFnZYFzf62mZG2WunjhvMDrC9LklUjNRQTE9GkT1MIPdWWdZqj"
ACCESS_TOKEN_KEY = "903283539860267009-8ndI3VdEEPUGO3K2uj6M8tYSWUFJRNT"
ACCESS_TOKEN_SECRET = "lcJd372YHdzTID26QvnqP2H1LHKkOB49ukEpEovMwbFOH"

saved_tickers = {}


@app.route('/', methods=["POST", "GET"])
def home_data():
    if request.method == "POST":
        ticker = request.form["ticker"]
        return redirect(url_for("get_twitter_data", ticker=ticker))

    ####################################################################

    return render_template("index.html")


@app.route('/<ticker>', methods=["POST", "GET"])
def get_twitter_data(ticker):

    if request.method == "POST":
        ticker = request.form["ticker"]
        return redirect(url_for("get_twitter_data", ticker=ticker))

    ############################################################################
    ts = TwitterSearch(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    search_obj = TwitterSearchOrder()
    search_obj.set_keywords([ticker, '$' + ticker, ticker + '$'])
    search_obj.set_language('en')
    search_obj.set_include_entities(False)
    search_obj.set_since(yesterday)
    search_obj.set_until(today)

    if ticker in saved_tickers:
        print(f'checking twitter for tweets of {ticker} (saved) ...')
        count_tweets = saved_tickers[ticker][today][0]
        percentage_sentiment = saved_tickers[ticker][today][1]
        sentiment = saved_tickers[ticker][today][2]

    else:
        count_tweets = 0
        print('checking twitter for tweets of {} ...'.format(ticker))
        for _ in ts.search_tweets_iterable(search_obj):
            count_tweets += 1

        print('there were {} tweets of {} today'.format(count_tweets, ticker))

        search_obj.set_negative_attitude_filter()
        count_negative = 0
        for _ in ts.search_tweets_iterable(search_obj):
            count_negative += 1

        print('according to twitter, there were {} negative tweets of {} today'.format(count_negative, ticker))

        search_obj.set_positive_attitude_filter()
        count_positive = 0
        for _ in ts.search_tweets_iterable(search_obj):
            count_positive += 1

        sum_of_sentiment = count_negative + count_positive
        if sum_of_sentiment != 0:
            percentage_sentiment = count_positive / sum_of_sentiment * 100
            if percentage_sentiment > 50:
                percentage_sentiment = str(int(percentage_sentiment)) + "%"
                sentiment = "positive"
            else:
                percentage_sentiment = str(int(percentage_sentiment)) + "%"
                sentiment = "negative"
        else:
            percentage_sentiment = "0%"
            sentiment = "positive"

        saved_tickers[ticker] = {today: [count_tweets, percentage_sentiment, sentiment]}

        print('according to twitter, there were {} positive tweets of {} today'.format(count_positive, ticker))

    ############################################################################
    ############################################################################
    reddit = praw.Reddit(client_id='fR7cRCGQceQ3DQ',
                         client_secret='NFFZcftp18b64hnADKBlMsJ3n1eFEw',
                         user_agent='Stonks',
                         username='stock2020',
                         password='stocks2020')
    subreddits = ['stocks', 'wallstreetbets']
    for i in range(len(subreddits)):
        subreddits[i] = reddit.subreddit(subreddits[i])
    reddit_mentions = search_ticker_mentions(ticker, subreddits, limit=100)
    ############################################################################
    return render_template("ticker.html", ticker=ticker, count_tweets=count_tweets,
                           percentage_sentiment=percentage_sentiment,
                           sentiment=sentiment,
                           reddit_mentions=reddit_mentions)


if __name__ == '__main__':
    app.run()
