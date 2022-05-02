from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
#from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
#app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key="a18RC9dAF80Sbm3fplVSMzbEn",
    api_secret="bbD1BMVnkP6R0Fvi9t16Q9Fjvc9JpU7cwHD8h0uOIgCwv2i7Zo",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])

if __name__ == "__main__":
    app.run()

