from flask import Flask, redirect, url_for, render_template, request
from TwitterSearch import *
from datetime import date, timedelta

app = Flask(__name__)

today = date.today()
yesterday = today-timedelta(1)


@app.route('/', methods=["POST", "GET"])
def home_data():

    consumer_key = "joSmtoOQCwLPD9bCcaX1c4voM"
    consumer_secret = "aFnZYFzf62mZG2WunjhvMDrC9LklUjNRQTE9GkT1MIPdWWdZqj"

    access_token_key = "903283539860267009-8ndI3VdEEPUGO3K2uj6M8tYSWUFJRNT"
    access_token_secret = "lcJd372YHdzTID26QvnqP2H1LHKkOB49ukEpEovMwbFOH"

    ts = TwitterSearch(consumer_key, consumer_secret, access_token_key, access_token_secret)

    search_obj = TwitterSearchOrder()
    search_obj.set_keywords(['TSLA', '$TSLA', 'TSLA$'])
    search_obj.set_language('en')
    search_obj.set_include_entities(False)
    search_obj.set_since(yesterday)
    search_obj.set_until(today)

    count_tweets = 0

    print('checking twitter for tweets of TSLA ...')

    for _ in ts.search_tweets_iterable(search_obj):
        count_tweets += 1

    print('there were {} tweets of TSLA today'.format(count_tweets))

    search_obj.set_negative_attitude_filter()
    count_negative = 0
    for _ in ts.search_tweets_iterable(search_obj):
        count_negative += 1

    print('according to twitter, there were {} negative tweets of TSLA today'.format(count_negative))

    search_obj.set_positive_attitude_filter()
    count_positive = 0
    for _ in ts.search_tweets_iterable(search_obj):
        count_positive += 1

    print('according to twitter, there were {} positive tweets of TSLA today'.format(count_positive))

    results = {'count_tweets': count_tweets, 'count_negative': count_negative, 'count_positive': count_positive}

    if request.method == "GET":
        return render_template("index.html", count_tweets=count_tweets)
    else:
        ticker = request.form["ticker"]
        return redirect(url_for("get_twitter_data", ticker=ticker))


@app.route('/<ticker>')
def get_twitter_data(ticker):

    consumer_key = "joSmtoOQCwLPD9bCcaX1c4voM"
    consumer_secret = "aFnZYFzf62mZG2WunjhvMDrC9LklUjNRQTE9GkT1MIPdWWdZqj"

    access_token_key = "903283539860267009-8ndI3VdEEPUGO3K2uj6M8tYSWUFJRNT"
    access_token_secret = "lcJd372YHdzTID26QvnqP2H1LHKkOB49ukEpEovMwbFOH"

    ts = TwitterSearch(consumer_key, consumer_secret, access_token_key, access_token_secret)

    search_obj = TwitterSearchOrder()
    search_obj.set_keywords([ticker, '$'+ticker, ticker+'$'])
    search_obj.set_language('en')
    search_obj.set_include_entities(False)
    search_obj.set_since(yesterday)
    search_obj.set_until(today)

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

    print('according to twitter, there were {} positive tweets of {} today'.format(count_positive, ticker))

    results = {'count_tweets': count_tweets, 'count_negative': count_negative, 'count_positive': count_positive}

    return render_template("ticker.html", ticker=ticker, count_tweets=count_tweets)


if __name__ == '__main__':
    app.run()