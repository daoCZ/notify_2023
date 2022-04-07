from flask import Flask, render_template, request
from googleapiclient.discovery import build
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
    output = request.form.to_dict()
    name = output["name"]
    request2 = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=name,
            type="channel"
        )
    response = request2.execute()
    response_list = response.get('items')
    channel_list = []
    for x in response_list:
        channel_list.append(x.get('snippet').get('channelTitle'))
    name = channel_list
    return render_template("home.html", name = name)
    #for x in response_list:
    #    print(x.get('snippet').get('channelTitle'))

if __name__ == '__main__':
    app.run(debug= True, port=5000)