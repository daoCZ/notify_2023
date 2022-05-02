from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
from flask_restful import Api
from authlib.integrations.flask_client import OAuth
import tweepy
import os

#import configparser
#import pandas as pd

api_key = 'AIzaSyDEvFHFs6x4mq7qlV-9nED16_BlZm_N5BE'
youtube = build('youtube', 'v3', developerKey = api_key)

app = Flask(__name__)

api = Api(app)

oauth = OAuth(app)

@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")


@app.route("/result", methods = ["POST", "GET"])

def result():
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
        youtube_entry = []
        youtube_entry.append(x.get('snippet').get('channelTitle'))
        youtube_entry.append(x.get('snippet').get('thumbnails').get('high').get('url'))
        youtube_entry.append("https://www.youtube.com/channel/" + x.get('snippet').get('channelId'))
        print(youtube_entry[2])
        youtube_list.append(youtube_entry)

    if youtube_list:
        name[0] = youtube_list
    else:
        name[0] = "No YouTube channel results for your search."
  
    #Twitter Procedures
    api_key = 'a18RC9dAF80Sbm3fplVSMzbEn'
    api_key_secret = 'bbD1BMVnkP6R0Fvi9t16Q9Fjvc9JpU7cwHD8h0uOIgCwv2i7Zo'

    access_token = '1511094339400835073-E84Wh4yaVDVP7hmDEEcPpevTrFjzRA'
    access_token_secret = 'kZpGnuhG5K92NcHCvbm1hDdkyR6JHNxNCce4MjoSB0KT2'
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    twitter_list = []
    users = api.search_users(q = namein, count=5)
    for user in users:
        id = user.id_str
        pic_url = user.profile_image_url
        twitter_item = []
        twitter_item.append(user.screen_name)
        twitter_item.append("https://twitter.com/i/user/" + id)
        twitter_item.append(pic_url)
        twitter_list.append(twitter_item)
    # user tweets
    #user = namein
    #limit=5
    #tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
    #twitter_list = []
    #for tweet in tweets:
    #   twitter_list.append([tweet.user.screen_name, tweet.full_text])

    if twitter_list:
        name[1] = twitter_list
    else:
        name[1] = "No Tweets from any account resulting from your search."

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


@app.route('/twitter/')
def twitter():
   
    # Twitter Oauth Config
    TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')
    oauth.register(
        name='twitter',
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)
 
@app.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    print(" Twitter User", profile)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug= True, port=5000)