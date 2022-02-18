from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Two drinks in...! Already feels like it's one of those nights to forget... the more that I drink, the more I feel broken, and alone..."


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
