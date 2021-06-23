import json

# /start
START_MSG = "Hello. This is start menu."
START_MENU = {"inline_keyboard": [
    [{"text": "Предложить пост", "callback_data": "suggest_post"},
     {"text": "Мои каналы", "callback_data": "my_channels"}],
    [{"text": "Отправленные сообщения", "callback_data": "sent_messages"}]]}

# suggest_post
SUGGEST_POST_MSG = "Suggest msg"
SUGGEST_POST_MENU = {"inline_keyboard": [
    [{"text": "Поиск", "callback_data": "search"},
     {"text": "Избранное", "callback_data": "favorites"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}

# search
SEARCH_MSG = "Введите название канала через @:"
SEARCH_MENU = {"inline_keyboard": [
    [{"text": "<< Назад", "callback_data": "back"}]]}
SEARCH_FAILED_MSG = "Канал не найден :(\nВозможна допущена ошибка в названии, " \
                    "либо канал не подключён к боту(\n" \
                    "Попробуйте ещё раз."

# after_search_not_favorites
AFTER_SEARCH_NOT_FAVORITES_MSG = "Канал успешно найден!"
AFTER_SEARCH_NOT_FAVORITES_MENU = {"inline_keyboard": [
    [{"text": "Добавить в избранное", "callback_data": "add_favorites"},
     {"text": "Предложить пост", "callback_data": "after_search_send_message_1"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}

# add_favorites
ADD_FAVORITES_MSG = "Канал успешно добавлен в избранное!"
ADD_FAVORITES_MENU = {"inline_keyboard": [
    [{"text": "Предложить пост", "callback_data": "after_search_send_message_2"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}

# after_search_send_message
AFTER_SEARCH_SEND_MESSAGE_MSG = "Пришлите пост для публикации в канал:"
AFTER_SEARCH_SEND_MESSAGE_MENU = {"inline_keyboard": [
    [{"text": "<< Назад", "callback_data": "back"}]]}

# message_sent
MESSAGE_SENT_MSG = "Сообщение успешно отправлено!"
MESSAGE_SENT_MENU = {"inline_keyboard": [
    [{"text": "Ещё один пост", "callback_data": "one_more_post"},
     {"text": "Назад в главное меню", "callback_data": "return_to_start"}]]}


# my_channels
MY_CHANNELS_MSG = "my channels msg"
MY_CHANNELS_MENU = {"inline_keyboard": [
    [{"text": "Подключить канал", "callback_data": "add_channel"},
     {"text": "Выбрать канал", "callback_data": "choose_channel"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}

# sent_messages
SENT_MSGS_MSG = "Выберите кол-во последних сообщений для просмотра:"
SENT_MSGS_MENU = {"inline_keyboard": [
    [{"text": "5", "callback_data": "sent_messages_looking|5"},
     {"text": "10", "callback_data": "sent_messages_looking|10"},
     {"text": "20", "callback_data": "sent_messages_looking|20"}],
    [{"text": "Все сообщения", "callback_data": "sent_messages_looking|all"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}





RETURN_BACK = {
    "suggest_post": "/start", "my_channels": "/start", "sent_messages": "/start",
    "search": "suggest_post",
    "search_done": "search", "add_favorites": "search",
    "after_search_send_message_1": "after_search_not_favorites", "after_search_send_message_2":  "add_favorites",
    "after_search_send_message_3": "suggest_post",

    "one_more_post": "after_search_send_message_3", "return_to_start": "/start"
}
