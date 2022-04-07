from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    print("test");
    return render_template("home.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

if __name__ == '__main__':
    app.run()