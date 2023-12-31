from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from googleapiclient.discovery import build
# from sqlalchemy import false
from flask_restful import Api
from authlib.integrations.flask_client import OAuth
import tweepy
import os
import pickle
from urllib import response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials

#import configparser
#import pandas as pd

api_key = 'AIzaSyDEvFHFs6x4mq7qlV-9nED16_BlZm_N5BE'
youtube = build('youtube', 'v3', developerKey = api_key)

CLIENT_SECRETS_FILE = "secretfile.json"

app = Flask(__name__)

api = Api(app)

oauth = OAuth(app)

toHTML = []
name2 = []
name = []
app.secret_key = b'_SDaf-e^d?\n\dscsd]'

 

@app.route('/')
@app.route("/home")
def home():
    global toHTML
    global name
    global name2
    if toHTML:
        if name2:
            if name:
                return render_template("home.html", infoYT=toHTML, name2=name2, name=name)
            else:
                return render_template("home.html", infoYT=toHTML, name2=name2)
        else:
            return render_template("home.html", infoYT=toHTML)
    elif name2:
        if name:
            return render_template("home.html", name2=name2, name=name)
        else:
            return render_template("home.html", name2=name2)
    elif name:
        return render_template("home.html", name=name)
    else:
        return render_template("home.html")


@app.route('/settings')
def settings():
    return render_template("settings.html")


@app.route("/result", methods = ["POST", "GET"])
def result():
    global toHTML
    global name
    global name2
    output = request.form.to_dict()
    namein = output["name"]
    name = ["",""]
    if(namein == ""):
        name[0] = "No query submitted."
        return render_template("home.html", name = name)
    request2 = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=namein,
            type="channel"
        )
    response = request2.execute()
    response_list = response.get('items')
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
    if toHTML:
        if name2:
            return render_template("home.html", infoYT=toHTML,  name = name, name2 = name2)
        else:
            return render_template("home.html", infoYT=toHTML,  name = name)
    elif name2:
        return render_template("home.html", name2=name2, name=name)
    else:
        return render_template("home.html", name = name)
    #for x in response_list:
    #    print(x.get('snippet').get('channelTitle'))

# from flask import json
# return render_template("sample.html",test=json.dumps(test))


allowRT = True 


@app.route("/twit_feed", methods = ["POST", "GET"])
def twit_feed():
    
    global name2
    global name
    global toHTML
    api_key = "a18RC9dAF80Sbm3fplVSMzbEn"
    api_key_secret =  "bbD1BMVnkP6R0Fvi9t16Q9Fjvc9JpU7cwHD8h0uOIgCwv2i7Zo"

    access_token = "1511094339400835073-E84Wh4yaVDVP7hmDEEcPpevTrFjzRA"
    access_token_secret = "kZpGnuhG5K92NcHCvbm1hDdkyR6JHNxNCce4MjoSB0KT2"
    output = request.form.to_dict()
    namein = output["name2"]
    if(namein == ""):
        return render_template("home.html", name2 = "No query submitted.")
    namein_noat = namein[1:]
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(api_key, api_key_secret)

    # set access to user's access key and access secret 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = ""
    try:
        user =api.get_user(screen_name = namein_noat)
    except:
        return render_template("home.html", name2 = 'No account match: check formatting: Ex: "@username".')
   
    id = user.id
    new_tweets = api.user_timeline(user_id=id,count=5, tweet_mode="extended")
    sname = namein
    count = 0
    result_set =[]
    result_item = []
    
    for status in tweepy.Cursor(api.user_timeline, screen_name=namein, tweet_mode="extended").items(5):
        result_item = []
        if allowRT == True:
            if(len(status._json.get('entities').get("user_mentions")) != 0):
                result_item.append(status._json.get('entities').get("user_mentions")[0].get('screen_name'))
                result_item.append(status.user.profile_image_url)
                result_item.append("https://twitter.com/twitter/statuses/" + status.id_str)
                result_item.append(status.created_at)
                result_item.append(status.full_text)
                count = count + 1
                result_set.append(result_item)
                continue
            else:
                result_item.append(sname)
                result_item.append(status.user.profile_image_url)
                result_item.append("https://twitter.com/twitter/statuses/" + status.id_str)
                result_item.append(status.created_at)
                result_item.append(status.full_text + "normal")
                count = count + 1
                result_set.append(result_item)
        
        if allowRT == False:
            if status.full_text.startswith("RT @") == False:
                result_item.append(sname)
                result_item.append(status.user.profile_image_url)
                result_item.append("https://twitter.com/twitter/statuses/" + status.id_str)
                result_item.append(status.created_at)
                result_item.append(status.full_text)
                count = count + 1
                result_set.append(result_item)

        if (count == 5):
            break
    
    if(len(result_set) != 0):
        name2 = result_set
    else:
        name2 = "No tweets available."
    if toHTML:
        if name:
            return render_template("home.html", infoYT=toHTML, name=name, name2=name2)
        else:
            return render_template("home.html", infoYt=toHTML, name2=name2)
    elif name:
        return render_template("home.html", name=name, name2=name2)
    else:
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



@app.route('/twit_feed/rt_filter/', methods=['POST']) 
def rt_filter():
    global allowRT 
    if allowRT == True:
        allowRT = False
        return "RTs blocked"
    else:
        allowRT = True 
        return "RTs allowed"
    #print("toggle!", flush=True)

# @app.route('/google/')
# def google():
@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes='https://www.googleapis.com/auth/youtube.readonly')

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)
@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes='https://www.googleapis.com/auth/youtube.readonly', state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('youTubeFeed'))

@app.route('/youTubeFeed')
def youTubeFeed():
    global toHTML
    global name2
    global name

    #token.pickle stores the users credentials from previously successful logins
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
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
    toHTML = ['','','','','']

    for x in range(5):
        request3 = youtube.activities().list(
            part="snippet,contentDetails",
            channelId= channel_dict[x],
            maxResults=1
        )

        response3 = request3.execute()    
        print(response3.get('items')[0].get('snippet').get('title'))
        title = response3.get('items')[0].get('snippet').get('title')
        print(response3.get('items')[0].get('snippet').get('thumbnails').get('default').get('url'))
        thumbnail = response3.get('items')[0].get('snippet').get('thumbnails').get('default').get('url')
        print(response3.get('items')[0].get('contentDetails').get('upload').get('videoId'))
        link = "https://www.youtube.com/watch?v="+ response3.get('items')[0].get('contentDetails').get('upload').get('videoId')
        print(response3.get('items')[0].get('snippet').get('publishedAt'))
        dateTime = response3.get('items')[0].get('snippet').get('publishedAt')
        print("")
        videoInfo = [title, thumbnail, link, dateTime]
        toHTML[x] = videoInfo

    if name2:
        if name:
            return render_template("home.html", name2=name2, infoYT=toHTML, name=name)
        else:
            return render_template("home.html", name2=name2, infoYT=toHTML)
    elif name:
        return render_template("home.html", name=name, infoYT=toHTML)
    else:
        return render_template("home.html", infoYT=toHTML)

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run(debug= True, port=5000)