from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from functools import partial
import os
import logging
import dialogflow_v2 as dialogflow
import telegram
import google


logger = logging.getLogger('tg_logger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update, context):
    update.message.reply_text('Hi!')


def answer(update, context, project_id):
    try:
        answer = detect_intent_text(
            project_id,
            update.effective_chat.id,
            update.message.text,
            'ru'
        )
    except google.api_core.exceptions.GoogleAPIError:
        logger.error(f'{__file__} Google API error')
    update.message.reply_text(answer.fulfillment_text)


def error(update, context, logger):
    logger.error(f'{__file__} Update {update} caused error {context.error}')


def run_bot(token, project_id, logger):
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(
        MessageHandler(Filters.text, partial(answer, project_id=project_id))
    )
    dp.add_error_handler(partial(error, logger=logger))
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
    return response.query_result


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    tg_logger_token = os.getenv('TG_LOGGER_TOKEN')
    tg_chat_id_logger = os.getenv('TG_CHAT_ID_LOGGER')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')

    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_logger_token, tg_chat_id_logger))

    run_bot(telegram_token, google_project_id, logger)


if __name__ == "__main__":
    main()
