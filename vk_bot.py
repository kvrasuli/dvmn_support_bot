import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
import logging
from tg_bot import detect_intent_text, TelegramLogsHandler
import google


def answer(event, vk_api, project_id, logger):
    try:
        answer = detect_intent_text(
            project_id,
            event.user_id,
            event.text,
            'ru'
        )
    except google.api_core.exceptions.GoogleAPIError:
        logger.error(f'{__file__} Google API error')

    if answer.intent.is_fallback:
        return
    try:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=random.randint(1, 1000)
        )
    except vk_api.exceptions.VkApiError:
        logger.error(f'{__file__} VK API error')


def run_bot(vk_group_token, logger):
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk_api_ = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api_, google_project_id, logger)


if __name__ == "__main__":
    load_dotenv()
    vk_group_token = os.getenv('VK_GROUP_TOKEN')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')

    tg_logger_token = os.getenv('TG_LOGGER_TOKEN')
    tg_chat_id_logger = os.getenv('TG_CHAT_ID_LOGGER')

    logger = logging.getLogger('tg_logger')
    logging.basicConfig(level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_logger_token, tg_chat_id_logger))

    run_bot(vk_group_token, logger)
