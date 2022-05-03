from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
from flask_restful import Api
from authlib.integrations.flask_client import OAuth
import tweepy
import os
import pickle
from urllib import response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

@app.route("/twit_feed", methods = ["POST", "GET"])
def twit_feed():
    api_key = "a18RC9dAF80Sbm3fplVSMzbEn"
    api_key_secret =  "bbD1BMVnkP6R0Fvi9t16Q9Fjvc9JpU7cwHD8h0uOIgCwv2i7Zo"

    access_token = "1511094339400835073-E84Wh4yaVDVP7hmDEEcPpevTrFjzRA"
    access_token_secret = "kZpGnuhG5K92NcHCvbm1hDdkyR6JHNxNCce4MjoSB0KT2"
    output = request.form.to_dict()
    namein = output["name2"]
    namein_noat = namein[1:]
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(api_key, api_key_secret)

    # set access to user's access key and access secret 
    auth.set_access_token(access_token, access_token_secret)


    api = tweepy.API(auth)

    user = api.get_user(screen_name=namein_noat)
    id = user.id

    new_tweets = api.user_timeline(user_id=id,count=5, tweet_mode="extended")
    #print(new_tweets)
    #print(api.get_user(user_id=id)._json.get('name'))

    #for tweet in new_tweets:
        #print(tweet._json.get("name"))
        #print(tweet._json.get("text"))

    sname = namein

    count = 0
    result_set =[]
    result_item = []

    for status in tweepy.Cursor(api.user_timeline, screen_name=namein, tweet_mode="extended").items():
        result_item = []
        if(len(status._json.get('entities').get("user_mentions")) == 0):
            result_item.append(sname)
            result_item.append(status.user.profile_image_url)
            result_item.append("https://twitter.com/twitter/statuses/" + status.id_str)
            result_item.append(status.created_at)
            result_item.append(status.full_text)
                            
            #print(sname)
            #print(status.user.profile_image_url)
            #print("https://twitter.com/twitter/statuses/" + status.id_str)
            #print(status.created_at)
            #print(status.full_text)
            #print()
            count = count + 1
            result_set.append(result_item)
            continue
        else:
            result_item.append(status._json.get('entities').get("user_mentions")[0].get('screen_name'))
            result_item.append(status.user.profile_image_url)
            result_item.append("https://twitter.com/twitter/statuses/" + status.id_str)
            result_item.append(status.created_at)
            result_item.append(status.full_text)
            count = count + 1
            result_set.append(result_item)
            #print(status.user.profile_image_url)
            #print(status._json.get('entities').get("user_mentions")[0].get('screen_name'))
            #print("https://twitter.com/twitter/statuses/" + status.id_str)
            #print(status.created_at)
            #print(status.full_text)
            #print()
        if (count == 5):
            break
    
    if(len(result_set) != 0):
        name2 = result_set
    else:
        name2 = "No tweets available."
    return render_template("home.html", name2 = name2)

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


@app.route('/google/')
def google_auth():
    credentials = None

    #token.pickle stores the users credentials from previously successful logins
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("secretfile.json",
                scopes = ['https://www.googleapis.com/auth/youtube.readonly']
                )

            flow.run_local_server(port=8090, prompt='consent', authorization_prompt_message="")

            credentials = flow.credentials

            with open("token.pickle", "wb") as f:
                pickle.dump(credentials, f)

    youtube = build("youtube", "v3", credentials=credentials)

    # request = youtube.playlistItems().list(
    #     part = "status", playlistId ="UUCezIgC97PvUuR4_gbFUs5g"
    # )



    request1 = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )

    response1 = request1.execute()

    request2 = youtube.subscriptions().list(
            part="snippet,contentDetails",
            channelId= response1.get('items')[0].get('id'),
            maxResults = 5
        )

    response2 = request2.execute()
    #print(response2)
    channel_dict = ['','','','','']
    for x in range(5):
        channel_dict[x] = response2.get('items')[x].get('snippet').get('resourceId').get('channelId')

    x = 0
    for x in range(5):
        request3 = youtube.activities().list(
            part="snippet,contentDetails",
            channelId= channel_dict[x],
            maxResults=1
        )

        response3 = request3.execute()    
        print(response3.get('items')[0].get('snippet').get('title'))
        print(response3.get('items')[0].get('snippet').get('thumbnails').get('default'))
        print(response3.get('items')[0].get('contentDetails').get('upload'))
        print(response3.get('items')[0].get('snippet').get('publishedAt'))
        print("hi!")

    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug= True, port=5000)