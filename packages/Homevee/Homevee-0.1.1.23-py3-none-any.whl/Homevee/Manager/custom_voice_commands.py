#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.Functions.condition_actions.actions import run_actions
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_voice_commands(db):
    rules = []
    results = Database.select_all("SELECT * FROM CUSTOM_VOICE_COMMANDS", {}, db)

    for item in results:
        commands = get_command_data(item['ID'], db)
        responses = get_response_data(item['ID'], db)

        rules.append({'id': item['ID'], 'name': item['NAME'], 'action_data': item['ACTION_DATA'],
                      'command_data': commands, 'response_data': responses})

    return {'rules': rules}

def get_command_data(id, db):
    items = Database.select_all("SELECT * FROM CUSTOM_VOICE_COMMAND_SENTENCES WHERE COMMAND_ID = :id", {'id': id}, db)

    data = []

    for item in items:
        data.append(item['COMMAND'])

    return data

def get_response_data(id, db):
    items = Database.select_all("SELECT * FROM CUSTOM_VOICE_COMMAND_RESPONSES WHERE COMMAND_ID = :id", {'id': id}, db)

    data = []

    for item in items:
        data.append(item['RESPONSE'])

    return data

def add_edit_voice_command(username, id, name, command_data, response_data, action_data, db):
    add_new = (id == None or id == "" or id == "-1")

    if(add_new):
        id = Database.insert("INSERT INTO CUSTOM_VOICE_COMMANDS (NAME, ACTION_DATA) VALUES (:name, :actions)",
                    {'name': name, 'actions': action_data}, db)

        command_data = json.loads(command_data)
        add_command_data(command_data, id, db)

        response_data = json.loads(response_data)
        add_response_data(response_data, id, db)
        return Status(type=STATUS_OK).get_dict()

    else:
        Database.update("UPDATE AUTOMATION_DATA SET NAME = :name, ACTION_DATA = :actions WHERE ID = :id",
            {'name': name, 'actions': action_data, 'id': id}, db)

        Database.delete("DELETE FROM CUSTOM_VOICE_COMMAND_SENTENCES WHERE COMMAND_ID = :id", {'id': id}, db)
        Database.delete("DELETE FROM CUSTOM_VOICE_COMMAND_RESPONSES WHERE COMMAND_ID = :id", {'id': id}, db)

        command_data = json.loads(command_data)
        add_command_data(command_data, id, db)

        response_data = json.loads(response_data)
        add_response_data(response_data, id, db)

        return Status(type=STATUS_OK).get_dict()

def delete_voice_command(username, id, db):
    Database.delete("DELETE FROM CUSTOM_VOICE_COMMANDS WHERE ID = :id", {'id': id}, db)
    Database.delete("DELETE FROM CUSTOM_VOICE_COMMAND_RESPONSES WHERE COMMAND_ID = :id", {'id': id}, db)
    Database.delete("DELETE FROM CUSTOM_VOICE_COMMAND_SENTENCES WHERE COMMAND_ID = :id", {'id': id}, db)

    return Status(type=STATUS_OK).get_dict()

def add_command_data(commands, id, db):
    for command in commands:
        param_array = {'id': id, 'command': command.lower()}

        Database.insert("""INSERT INTO CUSTOM_VOICE_COMMAND_SENTENCES (COMMAND_ID, COMMAND) VALUES (:id, :command)""",
            param_array)

def add_response_data(responses, id, db):
    for response in responses:
        param_array = {'id': id, 'response': response}

        Database.insert("""INSERT INTO CUSTOM_VOICE_COMMAND_RESPONSES (COMMAND_ID, RESPONSE) VALUES (:id, :response)""",
            param_array)

def run_custom_voice_commands(text, username, db):
    result = Database.select_one("SELECT * FROM CUSTOM_VOICE_COMMAND_SENTENCES, CUSTOM_VOICE_COMMANDS WHERE ID = COMMAND_ID AND COMMAND = :command",
                {'command': text}, db)

    if(result is None):
        return None

    id = result['ID']

    action_data = result['ACTION_DATA']

    action_data = json.loads(action_data)

    #run actions
    run_actions(action_data, db)

    result = Database.select_one("SELECT * FROM CUSTOM_VOICE_COMMAND_RESPONSES WHERE COMMAND_ID = :id ORDER BY RANDOM()",
                {'id': id}, db)

    return result['RESPONSE']