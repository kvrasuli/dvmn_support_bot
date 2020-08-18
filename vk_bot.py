import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import os
import random
from tg_bot import detect_intent_text


def answer(event, vk_api, project_id):
    answer = detect_intent_text(
        project_id,
        event.user_id,
        event.text,
        'ru'
    )
    if answer.intent.is_fallback:
        return
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_group_token = os.getenv('VK_GROUP_TOKEN')
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')
    vk_session = vk_api.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api, google_project_id)
