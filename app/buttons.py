import json

# /start
START_MSG = "Это стартовое меню!\n"
START_MENU = {"inline_keyboard": [
    [{"text": "Предложить пост", "callback_data": "suggest_post"},
     {"text": "Мои каналы", "callback_data": "my_channels"}]]}
   # [{"text": "Отправленные сообщения", "callback_data": "sent_messages"}]]}

# suggest_post
SUGGEST_POST_MSG = "Чтобы предложить пост - найдите канал с помощью поиска, " \
                   "если ещё не добавляли его в избранное."
SUGGEST_POST_MENU = {"inline_keyboard": [
    [{"text": "Поиск", "callback_data": "search"},
     {"text": "Избранное", "callback_data": "favorites"}],
    [{"text": "<< Назад", "callback_data": "back"}]]}

# favorites
MY_FAVORITES_MSG = "Ваши каналы, добавленные в избранное: "
MY_FAVORITES_MENU = [[{"text": "➖ Удалить канал", "callback_data": "delete_from_favorites"},
                     {"text": "<< Назад", "callback_data": "back"}]]

# delete_from_favorites
DELETE_FROM_FAVORITES_MSG = "Нажмите на канал, который хотите удалить из избранного:"
DELETE_FROM_FAVORITES_MENU = [[{"text": "<< Назад", "callback_data": "back"}]]
AFTER_DELETE_CHANNEL_FROM_FAVORITES_MSG = "Канал успешно удалён из избранного!"

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


# after_search_send_message
AFTER_SEARCH_SEND_MESSAGE_MSG = "Пришлите пост для публикации в канал:"
AFTER_SEARCH_SEND_MESSAGE_MENU = {"inline_keyboard": [
    [{"text": "<< Назад", "callback_data": "back"}]]}

# limit for messages
LIMIT = 5
# message_sent
MESSAGE_SENT_MSG = "Сообщение успешно отправлено!"
# message_not_sent
MESSAGE_NOT_SENT_MSG = "Вы отправили уже 5 сообщений, которые ещё не рассмотрели.\n" \
                       "Для того чтобы отправить новое сообщение удалите одно из уже отправленных, " \
                       "либо дождитесь когда создатель канала рассмотрит одно " \
                       "из ваших сообщений и удалит его из очереди."

# my_channels
MY_CHANNELS_MSG = "Здесь вы можете подключить новый канал к боту, либо выбрать уже подключенный."
MY_CHANNELS_MENU = [[{"text": "➕ Добавить канал", "callback_data": "connect_channel"},
                     {"text": "🔄 Обновить", "callback_data": "my_channels"}],
                    [{"text": "<< Назад", "callback_data": "back"}]]

# connect_channel
CONNECT_CHANNEL_MSG = "Для того чтобы добавить канал необходимо:\n" \
                      "1. Добавить бота в канал как администратора\n" \
                      "2. Убедиться в том, что у бота есть права для публикации постов\n" \
                      "3. Прислать название канала через @\n" \
                      "Если все шаги были выполнены успешно, то канал отобразится в списке каналов."
CONNECT_CHANNEL_MENU = {"inline_keyboard": [
    [{"text": "<< Назад", "callback_data": "back"}]]}



# # sent_messages
# SENT_MSGS_MSG = "Выберите кол-во последних сообщений для просмотра:"
# SENT_MSGS_MENU = {"inline_keyboard": [
#     [{"text": "5", "callback_data": "sent_messages_looking|5"},
#      {"text": "10", "callback_data": "sent_messages_looking|10"},
#      {"text": "20", "callback_data": "sent_messages_looking|20"}],
#     [{"text": "Все сообщения", "callback_data": "sent_messages_looking|all"}],
#     [{"text": "<< Назад", "callback_data": "back"}]]}



RETURN_BACK = {
    "suggest_post": "/start", "my_channels": "/start", "sent_messages": "/start",

    "search": "suggest_post", "favorites": "suggest_post",

    "delete_from_favorites": "favorites",

    "after_search_not_favorites": "search", "add_favorites": "search",
    "after_search_send_message_1": "after_search_not_favorites", "after_search_send_message_2": "search",
    "after_search_send_message_3": "favorites",
    
    "one_more_post": "after_search_send_message_3", "return_to_start": "/start",
    "message_not_sent": "suggest_post",


    "connect_channel": "my_channels",  "channel_for_looking_through_posts": "my_channels"

}
