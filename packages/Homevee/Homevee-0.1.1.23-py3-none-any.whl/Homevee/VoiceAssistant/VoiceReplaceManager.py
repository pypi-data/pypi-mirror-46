#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_voice_replace_items(user, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    replace = []

    results = Database.select_all("SELECT DISTINCT REPLACE_WITH FROM VOICE_COMMAND_REPLACE WHERE USERNAME = :user",
                {'user': user.username}, db)

    for item in results:
        items = Database.select_all("SELECT TEXT FROM VOICE_COMMAND_REPLACE WHERE REPLACE_WITH == :item AND USERNAME = :user",
            {'user': user.username, 'item': item['REPLACE_WITH']}, db)

        replacements = []

        for replacement in items:
            replacements.append(replacement['TEXT'])

        replace.append({'replacewith': item['REPLACE_WITH'], 'replacearray': replacements})

    return {'replacedata': replace}

def add_edit_voice_replace_item(user, replacewith, replaceitems, db):
    replaceitems = json.loads(replaceitems)

    Database.delete("DELETE FROM VOICE_COMMAND_REPLACE WHERE REPLACE_WITH = :replacewith AND USERNAME = :user",
                {'replacewith': replacewith, 'user': user.username}, db)

    for item in replaceitems:
        Database.insert("INSERT INTO VOICE_COMMAND_REPLACE (user, REPLACE_WITH, TEXT) VALUES (:user, :replacewith, :text)",
                    {'user': user.username, 'replacewith': replacewith, 'text': item}, db)

    return Status(type=STATUS_OK).get_dict()

def delete_voice_replace_item(user, replacewith, db):
    Database.delete("DELETE FROM VOICE_COMMAND_REPLACE WHERE REPLACE_WITH = :replacewith AND USERNAME = :user",
                {'replacewith': replacewith, 'user': user.username}, db)
    return Status(type=STATUS_OK).get_dict()