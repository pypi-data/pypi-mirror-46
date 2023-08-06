#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.Item.Room import Room
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_automations(user, room, db):
    if not user.has_permission(room):
        return {'result': 'nopermission'}

    rules = []
    results = Database.select_all("SELECT * FROM AUTOMATION_DATA WHERE LOCATION = :location", {'location': room}, db)

    for item in results:
        data = get_full_automation_data(item['ID'], db)

        if 'result' in data and data['result'] == 'nopermission':
            continue

        rules.append(data)

    return {'rules': rules}

def get_full_automation_data(id, db):
    data = Database.select_all("SELECT * FROM AUTOMATION_DATA WHERE ID = :id", {'id': id}, db)

    trigger_data = get_trigger_data(id, db)

    return {'name': data['NAME'], 'id': data['ID'], 'location': data['LOCATION'],
            'locationname': Room.get_name_by_id(data['LOCATION'], db), 'triggerdata': trigger_data,
            'conditiondata': data['CONDITION_DATA'], 'actiondata': data['ACTION_DATA'], 'isactive': True}

def get_trigger_data(id, db):
        items = Database.select_all("SELECT * FROM AUTOMATION_TRIGGER_DATA WHERE AUTOMATION_RULE_ID = :id", {'id': id}, db)

        trigger_data = []

        for item in items:
            trigger_data.append({'type': item['TYPE'], 'id': item['ID'], 'value': item['VALUE'], 'text': item['TEXT']})

        return trigger_data

def add_edit_automation_rule(user, location, id, name, trigger_data, condition_data, action_data, is_active, db):
    if not user.has_permission(location):
        return {'result': 'nopermission'}

    add_new = (id == None or id == "" or id == "-1")

    if(add_new):
        id = Database.insert("INSERT INTO AUTOMATION_DATA (LOCATION, NAME, CONDITION_DATA, ACTION_DATA, IS_ACTIVE) VALUES (:location, :name, :conditions, :actions, :active)",
                    {'location': location, 'name': name, 'conditions': condition_data, 'actions': action_data, 'active': is_active}, db)

        trigger_data = json.loads(trigger_data)

        add_trigger_data(trigger_data, id, db)
        return Status(type=STATUS_OK).get_dict()

    else:
        Database.update("UPDATE AUTOMATION_DATA SET LOCATION = :location, NAME = :name, CONDITION_DATA = :conditions, ACTION_DATA = :actions, IS_ACTIVE = :active WHERE ID = :id",
            {'location': location, 'name': name, 'conditions': condition_data, 'actions': action_data, 'active': is_active, 'id': id}, db)

        trigger_data = json.loads(trigger_data)

        Database.delete("DELETE FROM AUTOMATION_TRIGGER_DATA WHERE AUTOMATION_RULE_ID = :id", {'id': id}, db)

        add_trigger_data(trigger_data, id, db)
        return Status(type=STATUS_OK).get_dict()

def delete_automation_rule(user, id, db):
    Database.delete("DELETE FROM AUTOMATION_DATA WHERE ID = :id", {'id': id}, db)
    Database.delete("DELETE FROM AUTOMATION_TRIGGER_DATA WHERE AUTOMATION_RULE_ID = :id", {'id': id}, db)

    return Status(type=STATUS_OK).get_dict()

def add_trigger_data(data, id, db):
    for data in data:
        param_array = {'rule': id, 'type': data['type'], 'text': data['textdata']}

        if('id' in data):
            param_array['id'] = data['id']
        else:
            param_array['id'] = None

        if('value' in data):
            param_array['value'] = data['value']
        else:
            param_array['value'] = None

        Database.insert("""INSERT INTO AUTOMATION_TRIGGER_DATA (AUTOMATION_RULE_ID, TYPE, ID, VALUE, TEXT) 
        VALUES (:rule, :type, :id, :value, :text)""", param_array, db)