from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from functools import partial
import os
import logging
import dialogflow_v2 as dialogflow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi!')


def answer(update, context, params):
    answer = detect_intent_text(
        params['project_id'],
        params['chat_id'],
        update.message.text,
        'ru'
    )
    update.message.reply_text(answer)


def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')


def run_bot(token, project_id, chat_id):
    updater = Updater(token, use_context=True)
    params = {'project_id': project_id, 'chat_id': chat_id}
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(
        MessageHandler(Filters.text, partial(answer, params=params))
    )
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=text,
        language_code=language_code,
    )
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )
    return response.query_result.fulfillment_text


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')
    tg_user_id = os.getenv('TG_USER_ID')
    run_bot(telegram_token, google_project_id, tg_user_id)


if __name__ == "__main__":
    main()
