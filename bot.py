# encoding: utf-8
# Pregunta: esto qué es?
import os
import logging
import requests
import slack
import asyncio
import json
import ssl as ssl_lib
import certifi
import time
import uuid
from datetime import datetime
from onboarding_tutorial import OnboardingTutorial, CreateMessage
from application import Application
from textblock import TextBlock
from award import Award



class Bot:
    def __init__(self):
        self.slack_token = os.environ["SLACK_BOT_TOKEN"]
        self.sc = slack.WebClient(token=self.slack_token)
        self.id = self.get_bot_id()
        self.textblock = TextBlock()
        self.user_email = dict()
        self.awards = list()

    def get_bot_id(self):
        response = self.sc.api_call("users.list")
        members = response['members']
        for member in members:
            if member['real_name'] == "Badges Bot":
                return(f"<@{member['id']}>")

    def list_badges(self, web_client, channel_id):
        #web_client.chat_postMessage(channel=channel_id, text="badge list")
        r = requests.get('http://vituin-chat.iaas.ull.es/api/badges')

        badges = dict()
        for badge_id in r.json():
            uri = 'http://vituin-chat.iaas.ull.es/api/badge/' + badge_id + '/json'
            badges[badge_id] = dict()
            badge = badges[badge_id]
            r2 = requests.get(uri)
            badge_json = r2.json()
            badge['image'] = badge_json['image']
            badge['name'] = badge_json['name']

        badges_block = self.textblock.badges_text_block(badges)
        web_client.chat_postMessage(channel=channel_id, blocks=badges_block)

    async def award_badge(self, user_id, badge_name, wc, cid):
        if user_id not in self.user_email:
            self.user_email[user_id] = await self.get_email(user_id, wc, cid)

        newaward_json = dict()
        newaward_json['email'] = self.user_email[user_id]
        newaward_json['name'] = badge_name

        r = requests.post('http://vituin-chat.iaas.ull.es/api/newaward', json=newaward_json)

        print(r.text)

    async def get_email(self, user_id, wc, cid):
        response = await self.sc.api_call("users.list")
        members = response['members']
        for member in members:
            if member['id'] in user_id:
                return member['profile']['email']
bot = Bot()

@slack.RTMClient.run_on(event="message")
async def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".

    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")

    args = data['text'].split()
    print(args)

    if args.pop(0) == bot.id:
        if ' '.join(args) == "list badges":
            bot.list_badges(web_client, channel_id)
        if args[0] == 'award':
            args.pop(0)
            user_id = args.pop(0)
            badge_name = ' '.join(args)
            await bot.award_badge(user_id, badge_name, web_client, channel_id)

def start(loop):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context, run_async=True, loop=loop)
    loop.run_until_complete(rtm_client.start())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start(loop)
