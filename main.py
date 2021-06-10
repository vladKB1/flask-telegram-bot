import requests
import json

from app.models import *
from app import flask_app
from app import db
from flask import Flask
from flask import request
from app.config import *

data = {"url": WEBHOOK_URL}
url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/setWebHook"

requests.post(url, data)


@flask_app.route("/", methods=["POST"])
def receive():
    user_id = request.json["message"]["from"]["id"]
    username = request.json["message"]["from"]["username"]

    send_message("тык", user_id)
    return "OK"


def send_message(message, user_id):
    method = "sendMessage"

    token = BOT_TOKEN
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": user_id, "text": message, "reply_markup": json.dumps({ "keyboard": [ [ {"text": "Кнопка 1"} ] ] }) }
    requests.post(url, data=data)
    pass

flask_app.run()
