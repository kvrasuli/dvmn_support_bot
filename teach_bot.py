import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import os
import json
import copy


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


def teach_bot():
    load_dotenv()
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')
    intents = repack_intents('questions.json')
    print('Intents repacked')
    load_intents_to_agent(intents, google_project_id)
    print('Intents loaded to agent')
    teach_agent(google_project_id)
    print('Agent taught')


if __name__ == "__main__":
    teach_bot()
