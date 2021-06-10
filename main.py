import requests

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

    # by primary_key
    user = User.query.get(int(user_id))

    # by any field
    # user = User.query.filter(User.id == int(user_id)).first()
    # user = User.query.filter(User.id == int(user_id)).all()
    # user = User.query.filter(User.id == int(user_id)).last()

    if user is None:
        send_message("Who is?", user_id)
        user = User(id=int(user_id), username=username)
        db.session.add(user)
        db.session.commit()
    else:
        send_message(f"Hello {user.username}", user.id)

    send_message("hello", user_id)
    return "OK"


def send_message(message, user_id):
    method = "sendMessage"

    token = BOT_TOKEN
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": user_id, "text": message}
    requests.post(url, data=data)


flask_app.run()
