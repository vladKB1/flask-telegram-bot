import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin@postdb:5432/postdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


TELEGRAM_URL = "https://api.telegram.org"
BOT_TOKEN = os.getenv('BOT_TOKEN', '1847977944:AAGw_tfQwOCV6NlK2rzT17YGKwHHE6AN-Xo')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://9130c761e346.ngrok.io')

