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


#def delete_message():


def get_chat(chat_id):
    method = "getChat"
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": chat_id}
    return requests.post(url, data=data)


def get_chat_admin(chat_id):
    method = "getChatAdministrators"
    url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/{method}"
    data = {"chat_id": chat_id}
    return requests.post(url, data=data)


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


        if user.state == "search":
            if check_search(text):
                user.state_data = text
                db.session.commit()

                if not check_favorite(user_id, text):
                    user.state = "after_search_not_favorites"
                    db.session.commit()
                    send_message(AFTER_SEARCH_NOT_FAVORITES_MSG, user_id, json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))
                else:
                    user.state = "after_search_send_message_2"
                    db.session.commit()
                    send_message(AFTER_SEARCH_SEND_MESSAGE_MSG, user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))
            else:
                send_short_msg(SEARCH_FAILED_MSG, user_id)
                send_message(SEARCH_MSG, user_id, json.dumps(SEARCH_MENU))

        elif user.state.find("after_search_send_message") != -1:
            # only text messages. Need to upgrade for all types of content.
            send_post_to_channel(user_id, get_channel_id(user.state_data), text)
            send_message(MESSAGE_SENT_MSG, user_id, json.dumps(MESSAGE_SENT_MENU))

        elif user.state == "connect_channel":
            channel = Channel.query.filter(Channel.name == text).first()
            
            if channel is None:
                get_chat(text)
                response = json.loads(get_chat(text).content)

                if response["ok"]:
                    channel_id = response["result"]["id"]
                    name = response["result"]["username"]

                    response = json.loads(get_chat_admin(channel_id).content)
                    if response["ok"]:
                        for member in response["result"]:
                            if member["status"] == "creator":
                                admin_user = int(member["user"]["id"])
                                break

                        if admin_user == user_id:
                            # add check on if bot can make change
                            channel = Channel(channel_id=channel_id, name="@"+name, admin_user=admin_user)
                            db.session.add(channel)
                            db.session.commit()

            #delete_message()
            user.state = "my_channels"
            menu = update_channels_menu(user_id, MY_CHANNELS_MENU.copy())
            send_message(MY_CHANNELS_MSG, user_id, json.dumps(menu))

    return ""


def get_channel_id(channel_name):
    return Channel.query.filter(Channel.name == channel_name).first().channel_id


def add_favorites(user_id, channel_name):
    channel_id = get_channel_id(channel_name)
    userFavoritesRelation = UserFavoritesRelation(user_id=user_id, channel_id=channel_id)
    db.session.add(userFavoritesRelation)
    db.session.commit()


def check_search(channel_name):
    channel = Channel.query.filter(Channel.name == channel_name).first()
    if channel is None:
        return False
    else:
        return True


def check_favorite(user_id, channel_id):
    userFavoritesRelation = UserFavoritesRelation.query.filter(
        UserFavoritesRelation.user_id == user_id and UserFavoritesRelation.channel_id == channel_id).first()

    if userFavoritesRelation is None:
        return False
    else:
        return True


def send_post_to_channel(user_id, channel_id, text):
    post = Post(user_id=user_id, channel_id=channel_id, text=text)
    db.session.add(post)
    db.session.commit()


def update_channels_menu(user_id, menu):
    channels = Channel.query.filter(Channel.admin_user == user_id).all()
    for channel in channels:
        menu.append([{"text": channel.name, "callback_data": "channel_chose|" + str(channel.id)}])
    return {"inline_keyboard": menu}


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
    #elif rdata == "sent_messages":
    #    edit_message(SENT_MSGS_MSG, message_id, user_id, json.dumps(SENT_MSGS_MENU))

    # press suggest_post
    elif rdata == "search":
        edit_message(SEARCH_MSG, message_id, user_id, json.dumps(SEARCH_MENU))
    elif rdata == "favorites":
        pass

    # press '<< back' after common button for suggest post & channel not favorites
    elif rdata == "after_search_not_favorites":
        edit_message(AFTER_SEARCH_NOT_FAVORITES_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))
    # press add_favorites
    elif rdata == "add_favorites":
        add_favorites(user_id, user.state_data)
        edit_message(ADD_FAVORITES_MSG, message_id, user_id, json.dumps(ADD_FAVORITES_MENU))
    # common button for suggest post
    elif rdata.find("after_search_send_message") != -1:
        edit_message(AFTER_SEARCH_SEND_MESSAGE_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))

    # press my_channels
    elif rdata == "my_channels":
        menu = update_channels_menu(user_id, MY_CHANNELS_MENU.copy())
        edit_message(MY_CHANNELS_MSG, message_id, user_id, json.dumps(menu))
    # press connect_channel
    elif rdata == "connect_channel":
        edit_message(CONNECT_CHANNEL_MSG, message_id, user_id, json.dumps(CONNECT_CHANNEL_MENU))


flask_app.run()
