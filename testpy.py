from googleapiclient.discovery import build
api_key = 'AIzaSyDEvFHFs6x4mq7qlV-9nED16_BlZm_N5BE'
youtube = build('youtube', 'v3', developerKey = api_key)
request = youtube.channels().list(
    part = 'statistics',
    forUsername = 'pewdiepie'
    )
response = request.execute()
print(response.get('items'))