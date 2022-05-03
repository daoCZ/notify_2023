import os
import pickle
from urllib import response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

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
    print()