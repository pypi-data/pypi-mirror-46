#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Item.ChatMessage import ChatMessage
from Homevee.Utils.Database_NEW import Database


def get_chat_messages(user, time, limit, db: Database = None):
    if db is None:
        db = Database()
    messages = ChatMessage.load_all_by_time(time, limit)
    return {'messages': ChatMessage.list_to_dict(messages)}

def get_chat_image(user, imageid, db: Database = None):
    if db is None:
        db = Database()
    return

def send_chat_message(user, data, db: Database = None):
    if db is None:
        db = Database()
    message = ChatMessage(user, data)
    return message.send()