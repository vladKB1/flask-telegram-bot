import json


START_MSG = "Hello. This is start menu."
START_MENU = {"inline_keyboard": [
                [{"text": "Предложить пост", "callback_data": "suggest_post"},
                {"text": "Мои каналы", "callback_data": "my_channels"}]]}


SUGGEST_POST_MSG = "Сообщение"
SUGGEST_POST_MENU = {"inline_keyboard": [
                [{"text": "Поиск", "callback_data": "find"},
                {"text": "Избранное", "callback_data": "favorites"}],
                [{"text": "<< Назад", "callback_data": "back"}]]}


MY_CHANNELS_MSG = "Сообщение"
MY_CHANNELS_MENU = {"inline_keyboard": [[{"text": "*список каналов", "callback_data": "find"}]]}
def find_channels(user_id, rdata):
    pass
    #channels
    #send_message(SUGGEST_POST_MSG, user_id, json.dumps(SUGGEST_POST_MENU))




RETURN_BACK = {
    "suggest_post": "/start", "my_channels": "/start"
}
