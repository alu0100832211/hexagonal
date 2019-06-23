# encoding: utf-8
import os
import logging
import slack
import asyncio
import ssl as ssl_lib
import certifi
from onboarding_tutorial import OnboardingTutorial, CreateMessage
from application import Application



class Bot:
    def __init__(self, app: Application):
        self.app = app

    @slack.RTMClient.run_on(event="message")
    async def message(self, **payload):
        """Display the onboarding welcome message after receiving a message
        that contains "start".
        """

        data = payload["data"]
        web_client = payload["web_client"]
        channel_id = data.get("channel")

        print(f"Mensaje recibido de channel {channel_id}")
        user_id = data.get("user")
        text = data.get("text")

        params = text.split()

        if user_id is not None:
            web_client.chat_postMessage(channel=channel_id, text=f"Hola <@{user_id}> tu mensaje es {text}")

            if params.pop(0) == "<@UKMCDNT7X>":
                if params.pop(0) == "list":
                    badges_list=createmsg.badges_list(self.app.list_badges())
                    web_client.chat_postMessage(channel=channel_id, blocks=badges_list)

#        for idx, param in enumerate(params):
#            web_client.chat_postMessage(channel=channel_id, text=f"parametro {idx} {param}")

        if text and text.lower() == "start":
            return start_onboarding(web_client, user_id, channel_id)
        else:
            return

    async def start(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler())
        ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
        slack_token = os.environ["SLACK_BOT_TOKEN"]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        rtm_client = slack.RTMClient(
                token=slack_token, ssl=ssl_context, run_async=True, loop=loop)
        loop.run_until_complete(rtm_client.start())

if __name__ == '__main__':
    app = Application()

    bot = Bot(app)

    bot.start()
