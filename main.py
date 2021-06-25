import requests
import json
from time import sleep
import threading

from app.models import *
from app import flask_app
from app import db
from flask import Flask
from flask import request
from app.config import *
from app.buttons import *
from app.APImethod import *

data = {"url": WEBHOOK_URL}
url = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/setWebHook"
requests.post(url, data)


@flask_app.route("/", methods=["POST"])
def receive():
    try:
        if "callback_query" in request.json:
            buttons_processing(request.json["callback_query"]["data"])
            return ""

        if "message" in request.json:
            user_id = int(request.json["message"]["from"]["id"])
            username = request.json["message"]["from"]["username"]
            user = User.query.get(user_id)

            if "text" in request.json["message"]:
                text = request.json["message"]["text"]
                log(text)

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
                    delete_buttons(user_id, user.state_data)

                    if check_search(text):
                        user.state_data = text
                        db.session.commit()

                        if not check_favorite(user_id, get_channel_id(text)):
                            user.state = "after_search_not_favorites"
                            db.session.commit()
                            send_message(AFTER_SEARCH_NOT_FAVORITES_MSG, user_id,
                                         json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))
                        else:
                            response = send_message(AFTER_SEARCH_SEND_MESSAGE_MSG,
                                                    user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))
                            response = json.loads(response.content)
                            message_id = int(response["result"]["message_id"])

                            user.state = "after_search_send_message_2"
                            user.state_data = str(message_id) + "|" + AFTER_SEARCH_SEND_MESSAGE_MSG + \
                                              "|" + user.state_data
                            db.session.commit()
                    else:
                        send_short_msg(SEARCH_FAILED_MSG, user_id)
                        user.state = "suggest_post"
                        db.session.commit()
                        send_message(SUGGEST_POST_MSG, user_id, json.dumps(SUGGEST_POST_MENU))

                elif user.state.find("after_search_send_message") != -1:
                    delete_buttons(user_id, user.state_data)

                    channel_id = get_channel_id(user.state_data.split("|")[2])
                    if len(Post.query.filter(Post.user_id == user_id, Post.channel_id == channel_id).all()) > LIMIT:
                        send_short_msg(MESSAGE_NOT_SENT_MSG, user_id)
                    else:
                        send_post_to_channel(user_id, channel_id, text)
                        send_short_msg(MESSAGE_SENT_MSG, user_id)

                    user.state = "/start"
                    db.session.commit()
                    send_message(START_MSG, user_id, json.dumps(START_MENU))

                elif user.state == "connect_channel":
                    delete_buttons(user_id, user.state_data)

                    channel = Channel.query.filter(Channel.name == text).first()
                    if channel is None:
                        get_chat(text)
                        response = json.loads(get_chat(text).content)

                        if response["ok"]:
                            channel_id = int(response["result"]["id"])
                            name = response["result"]["username"]

                            response = json.loads(get_chat_admin(channel_id).content)
                            if response["ok"]:
                                for member in response["result"]:
                                    if member["status"] == "creator":
                                        admin_user = int(member["user"]["id"])
                                        break

                                if admin_user == user_id:
                                    channel = Channel(id=channel_id, name="@" + name, admin_user=admin_user)
                                    db.session.add(channel)
                                    db.session.commit()

                    user.state = "my_channels"
                    menu = update_channels_menu(user_id, MY_CHANNELS_MENU.copy(), "channel_for_looking_through_posts|")
                    send_message(MY_CHANNELS_MSG, user_id, json.dumps(menu))

                elif user.state == "waiting_edit_msg":
                    post = Post.query.filter(Post.id == int(user.state_data)).first()
                    post.text = text
                    db.session.commit()

                    user.state = "/start"
                    user.state_data = ""
                    db.session.commit()
                    send_message(START_MSG, user_id, json.dumps(START_MENU))

            return ""
        return ""
    except:
        return "BAD"


def log(message):
    print(message)


def delete_buttons(user_id, state_data):
    message_id = int(state_data.split("|")[0])
    msg = state_data.split("|")[1]
    edit_message_short(msg, message_id, user_id)


def check_my_channels():
    users = User.query.all()

    for user in users:
        channels = Channel.query.filter(Channel.admin_user == user.id).all()
        for channel in channels:
            response = json.loads(get_chat_admin(channel.id).content)
            if not response["ok"]:
                Channel.query.filter(Channel.id == channel.id).delete()
                db.session.commit()


def get_username(user_id):
    return User.query.get(user_id).username


def get_channel_id(channel_name):
    return Channel.query.filter(Channel.name == channel_name).first().id


def get_channel_name(channel_id):
    return Channel.query.get(channel_id).name


def check_search(channel_name):
    channel = Channel.query.filter(Channel.name == channel_name).first()
    if channel is None:
        return False
    else:
        return True


def add_favorites(user_id, channel_name):
    channel_id = get_channel_id(channel_name)
    userFavoritesRelation = UserFavoritesRelation(user_id=user_id, channel_id=channel_id)
    db.session.add(userFavoritesRelation)
    db.session.commit()


def delete_favorites(user_id, channel_id):
    UserFavoritesRelation.query.filter(UserFavoritesRelation.user_id == user_id,
                                       UserFavoritesRelation.channel_id == channel_id).delete()
    db.session.commit()


def check_favorite(user_id, channel_id):
    userFavoritesRelation = UserFavoritesRelation.query.filter(
        UserFavoritesRelation.user_id == user_id,
        UserFavoritesRelation.channel_id == channel_id).first()
    if userFavoritesRelation is None:
        return False
    else:
        return True


def send_post_to_channel(user_id, channel_id, text):
    post = Post(user_id=user_id, channel_id=channel_id, text=text)
    db.session.add(post)
    db.session.commit()


# update/get menus
def update_favorites_menu(user_id, menu, callback_text):
    channels = UserFavoritesRelation.query.filter(UserFavoritesRelation.user_id == user_id).all()
    for channel in channels:
        menu.append([{"text": get_channel_name(channel.channel_id),
                      "callback_data": callback_text + str(channel.channel_id)}])
    return {"inline_keyboard": menu}


def update_channels_menu(user_id, menu, callback_text):
    channels = Channel.query.filter(Channel.admin_user == user_id).all()
    for channel in channels:
        menu.append([{"text": channel.name, "callback_data": callback_text + str(channel.id)}])
    return {"inline_keyboard": menu}


def get_post_menu(post_id):
    menu = [[{"text": "✅ Опубликовать", "callback_data": "publish_post|" + str(post_id)},
             {"text": "❌ Удалить", "callback_data": "delete_post|" + str(post_id)}]]
    return {"inline_keyboard": menu}


def get_user_post_menu(post_id):
    menu = [[{"text": "Изменить", "callback_data": "edit_post|" + str(post_id)},
             {"text": "❌ Удалить", "callback_data": "delete_post|" + str(post_id)}]]
    return {"inline_keyboard": menu}


def buttons_processing(rdata):
    user_id = int(request.json["callback_query"]["from"]["id"])
    username = request.json["callback_query"]["from"]["username"]
    user = User.query.get(user_id)
    message_id = request.json["callback_query"]["message"]["message_id"]

    if rdata == "back":
        if user.state == "channel_for_looking_through_posts":
            messages = user.state_data.split("|")
            for msg_id in messages:
                delete_message(user_id, msg_id)
        elif user.state == "sent_messages":
            messages = user.state_data.split("|")
            for i in range(len(messages) - 2):
                msg_id = messages[i]
                delete_message(user_id, int(msg_id))

        rdata = RETURN_BACK[user.state]
    elif rdata == "one_more_post" or rdata == "return_to_start":
        rdata = RETURN_BACK[rdata]

    if rdata.find("publish_post") != -1:
        post_id = rdata.split("|")[1]
        post = Post.query.get(post_id)
        send_short_msg(post.text, post.channel_id)
        Post.query.filter(Post.id == post_id).delete()
        db.session.commit()
        delete_message(user_id, message_id)
        return ""
    elif rdata.find("delete_post") != -1:
        Post.query.filter(Post.id == rdata.split("|")[1]).delete()
        db.session.commit()
        delete_message(user_id, message_id)
        return ""
    elif rdata.find("edit_post") != -1:
        post = Post.query.filter(Post.id == rdata.split("|")[1]).first()

        messages = user.state_data.split("|")
        for msg_id in messages:
            delete_message(user_id, msg_id)

        msg = f"Channel: @{get_channel_name(post.channel_id)}\n\n" + post.text  \
              + "\n\n Пришлите исправленное сообщение: "
        send_short_msg(msg, user_id)

        user.state = "waiting_edit_msg"
        user.state_data = str(post.id)
        db.session.commit()
        return ""


    user.state = rdata
    db.session.commit()

    if rdata == "/start":
        edit_message(START_MSG, message_id, user_id, json.dumps(START_MENU))
    elif rdata == "suggest_post":
        edit_message(SUGGEST_POST_MSG, message_id, user_id, json.dumps(SUGGEST_POST_MENU))


    # press search
    elif rdata == "search":
        user.state_data = str(message_id) + "|" + SEARCH_MSG
        db.session.commit()
        edit_message(SEARCH_MSG, message_id, user_id, json.dumps(SEARCH_MENU))

    # after_search_not_favorites
    elif rdata == "after_search_not_favorites":
        edit_message(AFTER_SEARCH_NOT_FAVORITES_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_NOT_FAVORITES_MENU))

    # press add_favorites
    elif rdata == "add_favorites":
        add_favorites(user_id, user.state_data)
        edit_message_short(ADD_FAVORITES_MSG, message_id, user_id)
        user.state = "suggest_post"
        send_message(SUGGEST_POST_MSG, user_id, json.dumps(SUGGEST_POST_MENU))



    # press favorites
    elif rdata == "favorites":
        menu = update_favorites_menu(user_id, MY_FAVORITES_MENU.copy(), "channel_chose|")
        edit_message(MY_FAVORITES_MSG, message_id, user_id, json.dumps(menu))

    # press delete_from_favorites
    elif rdata == "delete_from_favorites":
        menu = update_favorites_menu(user_id, DELETE_FROM_FAVORITES_MENU.copy(), "channel_delete|")
        edit_message(DELETE_FROM_FAVORITES_MSG, message_id, user_id, json.dumps(menu))

    # delete channel from favorites
    elif rdata.find("channel_delete") != -1:
        channel_id = int(rdata.split("|")[1])
        delete_favorites(user_id, channel_id)
        menu = update_favorites_menu(user_id, MY_FAVORITES_MENU.copy(), "channel_chose|")
        edit_message(AFTER_DELETE_CHANNEL_FROM_FAVORITES_MSG, message_id, user_id, json.dumps(menu))

    # chose channel from favorites
    elif rdata.find("channel_chose") != -1:
        user.state_data = get_channel_name(int(rdata.split("|")[1]))
        buttons_processing("after_search_send_message_3")

    # after_search_send_message_###
    elif rdata.find("after_search_send_message") != -1:
        user.state_data = str(message_id) + "|" + AFTER_SEARCH_SEND_MESSAGE_MSG + "|" + user.state_data
        db.session.commit()
        edit_message(AFTER_SEARCH_SEND_MESSAGE_MSG, message_id, user_id, json.dumps(AFTER_SEARCH_SEND_MESSAGE_MENU))



    # my_channels
    elif rdata == "my_channels":
        check_my_channels()
        menu = update_channels_menu(user_id, MY_CHANNELS_MENU.copy(), "channel_for_looking_through_posts|")
        edit_message(MY_CHANNELS_MSG, message_id, user_id, json.dumps(menu))

    # connect_channel
    elif rdata == "connect_channel":
        user.state_data = str(message_id) + "|" + CONNECT_CHANNEL_MSG
        db.session.commit()
        edit_message(CONNECT_CHANNEL_MSG, message_id, user_id, json.dumps(CONNECT_CHANNEL_MENU))

    # channel_for_looking_through_posts
    elif rdata.find("channel_for_looking_through_posts") != -1:
        delete_message(user_id, message_id)

        channel_id = int(rdata.split("|")[1])
        posts = Channel.query.get(channel_id).posts
        user.state = "channel_for_looking_through_posts"
        user.state_data = ""
        db.session.commit()

        for post in posts:
            msg = f"Author: @{get_username(post.user_id)}\n\n" + post.text
            menu = get_post_menu(post.id)
            response = send_message(msg, user_id, json.dumps(menu))

            response = json.loads(response.content)
            user.state_data += str(response["result"]["message_id"]) + "|"
            db.session.commit()


        msg = f"У вас {len(posts)} предложенных постов без ответа."
        menu = {"inline_keyboard": [[{"text": "<< Назад", "callback_data": "back"}]]}
        send_message(msg, user_id, json.dumps(menu))

    elif rdata == "sent_messages":
        delete_message(user_id, message_id)

        user.state_data = ""
        db.session.commit()

        for post in user.posts:
            msg = f"Channel: @{get_channel_name(post.channel_id)}\n\n" + post.text
            menu = get_user_post_menu(post.id)
            response = send_message(msg, user_id, json.dumps(menu))

            response = json.loads(response.content)
            user.state_data += str(response["result"]["message_id"]) + "|"
            db.session.commit()

        msg = f"У вас {len(user.posts)} необработанных сообщений:"
        menu = {"inline_keyboard": [[{"text": "<< Назад", "callback_data": "back"}]]}
        response = send_message(msg, user_id, json.dumps(menu))

        response = json.loads(response.content)
        user.state_data += str(response["result"]["message_id"]) + "|"
        db.session.commit()


def async_check_channels():
    while(True):
        sleep(120)

        users = User.query.all()
        for user in users:
            channels = Channel.query.filter(Channel.admin_user == user.id).all()
            for channel in channels:
                response = json.loads(get_chat_admin(channel.id).content)
                if not response["ok"]:
                    Channel.query.filter(Channel.id == channel.id).delete()
                    db.session.commit()


async_method = threading.Thread(target=async_check_channels)
async_method.start()

flask_app.run()
# flask_app.run(host="0.0.0.0")
