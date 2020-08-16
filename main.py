from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
from dotenv import load_dotenv
import os
import logging
import dialogflow_v2 as dialogflow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def echo(update, context):
    update.message.reply_text(update.message.text)
    

def answer(update, context):
    answer = detect_intent_texts('dvmnsupportbot-286611', '324357215', update.message.text, 'ru')
    update.message.reply_text(answer)


def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')


def run_bot(token):
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, answer))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    run_bot(telegram_token)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text


if __name__ == "__main__":
    main()
