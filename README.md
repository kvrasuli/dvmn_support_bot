# Support vk & telegram bot

This is a telegram and vk support bots using Google dialogflow.

### How to use

You'll need you own Devman API token, Telegram API token and your chat ID.
Create 4 corresponding environment variables:
```
TELEGRAM_TOKEN='your notification bot token'
GOOGLE_APPLICATION_CREDENTIALS='path to your google cloud json key'
GOOGLE_PROJECT_ID='your google cloud project id'
VK_GROUP_TOKEN='your vk group token'
```
Add 2 additional env variables for logging:
```
TG_CHAT_ID_LOGGER='your tg chat id'
TG_LOGGER_TOKEN='your tg logger bot'
```
To teach dialogflow agent run teach_bot.py with
```
python3 teach_bot.py
```
To run the tg bot launch tg_bot.py script with the following console command:
```
python3 tg_bot.py
```
To run the vk bot launch vk_bot.py script:
```
python3 vk_bot.py
```
### What it looks like

[gif link]

### Deploy

Procfile for heroku deploying is created. Use this guide to deploy:
https://devcenter.heroku.com/articles/github-integration

Add this addition buildpack in settings:
https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack

### How to install dependencies

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip3 install -r requirements.txt
```
