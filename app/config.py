import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://db_user:123@localhost:5432/db_flask_telegram_bot"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


TELEGRAM_URL = "https://api.telegram.org"
BOT_TOKEN = os.getenv('BOT_TOKEN', '1847977944:AAGw_tfQwOCV6NlK2rzT17YGKwHHE6AN-Xo')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://3f9aab80c6fa.ngrok.io')

