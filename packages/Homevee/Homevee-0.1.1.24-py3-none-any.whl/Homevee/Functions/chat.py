#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Item.ChatMessage import ChatMessage


def get_chat_messages(user, time, limit, db):
    messages = ChatMessage.load_all_by_time(time, limit, db)
    return {'messages': ChatMessage.list_to_dict(messages)}

def get_chat_image(user, imageid, db):
    return

def send_chat_message(user, data, db):
    message = ChatMessage(user, data)
    return message.send()