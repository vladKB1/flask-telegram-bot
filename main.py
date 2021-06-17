import requests
import json

from app.models import *
from app import flask_app
from app import db
from flask import Flask
from flask import request
from app.config import *
from app.buttons import *

data = {"url": WEBHOOK_URL}
url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/setWebHook"
requests.post(url, data)


def send_message(message, user_id):
    method = "sendMessage"
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": user_id, "text": message}
    requests.post(url, data=data)


def send_message(message, user_id, reply_markup):
    method = "sendMessage"
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": user_id, "text": message, "reply_markup": reply_markup}
    requests.post(url, data=data)


def edit_message(message, message_id, user_id, reply_markup):
    method = "editMessageText"
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": user_id, "message_id": message_id, "text": message, "reply_markup": reply_markup}
    requests.post(url, data=data)


@flask_app.route("/", methods=["POST"])
def receive():
    if "callback_query" in request.json:
        buttons_processing()
        return ""

    user_id = int(request.json["message"]["from"]["id"])
    username = request.json["message"]["from"]["username"]
    user = User.query.get(user_id)

    if "text" in request.json["message"]:
        text = request.json["message"]["text"]
        if text == "/start":
            if user is None:
                user = User(id=user_id, username=username)
                db.session.add(user)
                db.session.commit()

            user.state = "/start"
            db.session.commit()
            send_message(START_MSG, user_id, json.dumps(START_MENU))

    return ""


def buttons_processing():
    user_id = int(request.json["callback_query"]["from"]["id"])
    username = request.json["callback_query"]["from"]["username"]
    user = User.query.get(user_id)
    message_id = request.json["callback_query"]["message"]["message_id"]
    rdata = request.json["callback_query"]["data"]

    if rdata == "back":
        rdata = RETURN_BACK[user.state]

    user.state = rdata
    db.session.commit()

    if rdata == "/start":
        edit_message(START_MSG, message_id, user_id, json.dumps(START_MENU))
    elif rdata == "suggest_post":
        edit_message(SUGGEST_POST_MSG, message_id, user_id, json.dumps(SUGGEST_POST_MENU))
    elif rdata == "my_channels":
        edit_message(SUGGEST_POST_MSG, message_id, user_id, json.dumps(SUGGEST_POST_MENU))

    # press suggest_post
    elif rdata == "find":
        find_channels(user_id)
        edit_message(SUGGEST_POST_MSG, message_id, user_id, json.dumps(SUGGEST_POST_MENU))
    elif rdata == "favorites":
        pass

    # my_channels
    # elif rd


flask_app.run()
