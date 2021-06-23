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


def send_short_msg(message, user_id):
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

        if user.state == "search":
            if check_search(text):
                user.state = "search_done"
                db.session.commit()

                if not check_favorite(text):
                    send_message(AFTER_SEARCH_NOT_FAVORITES_MSG, user_id, json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))
                else:
                    send_message(AFTER_SEARCH_SEND_MESSAGE_MSG, user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))
            else:
                send_short_msg(SEARCH_FAILED_MSG, user_id)
                send_message(SEARCH_MSG, user_id, json.dumps(SEARCH_MENU))
        elif user.state.find("after_search_send_message") != -1: #only text messages. Need to upgrade for all types of content.
            send_message_to_channel(text)

            user.state = "message_sent"
            db.session.commit()
            send_message(MESSAGE_SENT_MSG, user_id, json.dumps(MESSAGE_SENT_MENU))
    return ""


def buttons_processing():
    user_id = int(request.json["callback_query"]["from"]["id"])
    username = request.json["callback_query"]["from"]["username"]
    user = User.query.get(user_id)
    message_id = request.json["callback_query"]["message"]["message_id"]
    rdata = request.json["callback_query"]["data"]

    if rdata == "back":
        rdata = RETURN_BACK[user.state]
    elif rdata == "one_more_post" or rdata == "return_to_start":
        rdata = RETURN_BACK[rdata]

    user.state = rdata
    db.session.commit()

    if rdata == "/start":
        edit_message(START_MSG, message_id, user_id, json.dumps(START_MENU))
    elif rdata == "suggest_post":
        edit_message(SUGGEST_POST_MSG, message_id, user_id, json.dumps(SUGGEST_POST_MENU))
    elif rdata == "my_channels":
        edit_message(MY_CHANNELS_MSG, message_id, user_id, json.dumps(MY_CHANNELS_MENU))
    elif rdata == "sent_messages":
        edit_message(SENT_MSGS_MSG, message_id, user_id, json.dumps(SENT_MSGS_MENU))

    # press suggest_post
    elif rdata == "search":
        edit_message(SEARCH_MSG, message_id, user_id, json.dumps(SEARCH_MENU))
    elif rdata == "favorites":
        pass

    # press back in after_search_not_favorites
    elif rdata == "after_search_not_favorites":
        edit_message(AFTER_SEARCH_NOT_FAVORITES_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))

    # press add_favorites
    elif rdata == "add_favorites":
        # add_favorites()
        edit_message(ADD_FAVORITES_MSG, message_id, user_id, json.dumps(ADD_FAVORITES_MENU))

    # press after_search_send_message
    elif rdata.find("after_search_send_message") != -1:
        edit_message(AFTER_SEARCH_SEND_MESSAGE_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))

def check_search(channel_name):
    channel = Channel.query.filter(Channel.name == channel_name).first()
    if channel is None:
        return False
    else:
        return True

def check_favorite(channel_name):
    # get info from UserFavoritesRelation
    return False

def send_message_to_channel(message):
    pass

flask_app.run()
