import configparser
import json
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import (PeerChannel)
# from telegram_channel_dictionary import german_nazi_chats_urls #dictionary of german nazi channels
import sys
from os import path
# sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
#from horror import prompt_continue, prompt_option


api_id = 3120822
api_hash = 'a6338609c7fbf970f15ff8b2d0d8342e'


with TelegramClient('tele', api_id, api_hash) as client:
    channels = json.load(open("app/config/telegram/telegramChannels.json"))
    options = list(channels.values())
    for channel in options:
        entity = client.get_entity(channel)  # the channel to scrape from
        messages = client.get_messages(entity)  # 80 recent messages
        print(entity)
        print(messages)

    client.run_until_disconnected()
