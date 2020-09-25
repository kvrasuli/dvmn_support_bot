import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import json
import copy
import logging
from tg_bot import TelegramLogsHandler
import google
import sys


def repack_intents(filename):
    with open(filename, 'r', encoding='utf8') as q:
        questions = json.load(q)
    intents = []
    intent = {
        "display_name": None,
        "messages": [{"text": {"text": [None]}}],
        "training_phrases": []
    }
    for key in questions:
        temp_intent = copy.deepcopy(intent)
        temp_intent['display_name'] = key
        temp_intent['messages'][0]['text']['text'][0] = questions[key]['answer']
        for question in questions[key]['questions']:
            training_phrase = {'parts': [{'text': question}]}
            temp_intent['training_phrases'].append(training_phrase)
        intents.append(temp_intent)
    return intents


def load_intents_to_agent(intents, project_id):
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(project_id)
    for intent in intents:
        client.create_intent(parent, intent)


def teach_agent(project_id):
    client = dialogflow.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


def teach_bot(google_project_id, logger):
    intents = repack_intents('questions.json')
    logger.info('Intents repacked')
    load_intents_to_agent(intents, google_project_id)
    logger.info('Intents loaded to agent')
    teach_agent(google_project_id)
    logger.info('Agent taught')


def main():
    load_dotenv()
    tg_logger_token = os.getenv('TG_LOGGER_TOKEN')
    tg_chat_id_logger = os.getenv('TG_CHAT_ID_LOGGER')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')
    logger = logging.getLogger('tg_logger')
    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_logger_token, tg_chat_id_logger))
    try:
        teach_bot(google_project_id, logger)
    except google.api_core.exceptions.InvalidArgument:
        logger.error(f'{__file__} Loading intents error')
        sys.exit()
    except google.api_core.exceptions.GoogleAPIError:
        logger.error(f'{__file__} Teaching agent error')
        sys.exit()


if __name__ == "__main__":
    main()
