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
        flow = InstalledAppFlow.from_client_secrets_file("secret_file.json",
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

request = youtube.activities().list(
        part="snippet,contentDetails",
        channelId="UCNFQ5O2rCsa75L6qHiusC-Q",
        maxResults=1
    )

response = request.execute()

print(response)

