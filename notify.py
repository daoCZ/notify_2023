from flask import Flask, render_template, request
from googleapiclient.discovery import build
import tweepy
#import configparser
#import pandas as pd

api_key = 'AIzaSyDEvFHFs6x4mq7qlV-9nED16_BlZm_N5BE'
youtube = build('youtube', 'v3', developerKey = api_key)

app = Flask(__name__)


@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")


@app.route("/result", methods = ["POST", "GET"])
def result():
    error = False
    output = request.form.to_dict()
    namein = output["name"]
    request2 = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=namein,
            type="channel"
        )
    response = request2.execute()
    response_list = response.get('items')
    name = ["",""]
    youtube_list = []
    for x in response_list:
        youtube_list.append(x.get('snippet').get('channelTitle'))
    if youtube_list:
        name[0] = youtube_list
    else:
        name[0] = "No YouTube channel results for your search."

    #Twitter Procedures
    api_key = 'dpCeHm2DJEwkvCpvtY6ihHQ5k'
    api_key_secret = '9vQly1Ep2g0YFZC1vkgiWG1g6rw3QR6PTyLlAzoDD1ClevYMkq'

    access_token = '1511094339400835073-To1THLCtzO59Sr4qZnHtGYKvKy1NXt'
    access_token_secret = 'hsWJEc7bYsrpabn78rRrP6jkbRlc4qESZXnIlbzREkUFY'
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # user tweets
    user = namein
    limit=5
    tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
    twitter_list = []
    for tweet in tweets:
        twitter_list.append([tweet.user.screen_name, tweet.full_text])

    if twitter_list:
        name[1] = twitter_list
    else:
        name[1] = "No Tweets from any account resulting from your search."

    print(name)
    return render_template("home.html", name = name)
    #for x in response_list:
    #    print(x.get('snippet').get('channelTitle'))

# from flask import json
# return render_template("sample.html",test=json.dumps(test))

@app.route("/tw_result", methods = ["POST", "GET"])
def tw_result():
    output = request.form.to_dict()
    namein = output["name"]


    #Twitter Code below
    api_key = 'dpCeHm2DJEwkvCpvtY6ihHQ5k'
    api_key_secret = '9vQly1Ep2g0YFZC1vkgiWG1g6rw3QR6PTyLlAzoDD1ClevYMkq'

    access_token = '1511094339400835073-To1THLCtzO59Sr4qZnHtGYKvKy1NXt'
    access_token_secret = 'hsWJEc7bYsrpabn78rRrP6jkbRlc4qESZXnIlbzREkUFY'

    #config = configparser.ConfigParser()
    #config.read('config.ini')

    #api_key = config['twitter']['api_key']
    #api_key_secret = config['twitter']['api_key_secret']

    #access_token = config['twitter']['access_token']
    #access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # user tweets
    user = namein
    limit=5

    tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)

    # tweets = api.user_timeline(screen_name=user, count=limit, tweet_mode='extended')

    # create DataFrame
    columns = ['User', 'Tweet']
    data = []

    for tweet in tweets:
        data.append([tweet.user.screen_name, tweet.full_text])

    if data:
        name = data
    else:
        name = "Twitter channel with name - "
        name += namein
        name += " - DOES NOT EXIST" 

    return render_template("home.html", name = name)
    #df = pd.DataFrame(data, columns=columns)


if __name__ == '__main__':
    app.run(debug= True, port=5000)