from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')


def run_bot(token):
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    run_bot(telegram_token)


if __name__ == "__main__":
    main()

