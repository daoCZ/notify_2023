from googleapiclient.discovery import build
api_key = 'AIzaSyDEvFHFs6x4mq7qlV-9nED16_BlZm_N5BE'
youtube = build('youtube', 'v3', developerKey = api_key)

def channel_search(user_query):
    youtube = build('youtube', 'v3', developerKey = api_key)
    request = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=user_query,
            type="channel"
        )
    response = request.execute()
    response_list = response.get('items')
    return response_list

