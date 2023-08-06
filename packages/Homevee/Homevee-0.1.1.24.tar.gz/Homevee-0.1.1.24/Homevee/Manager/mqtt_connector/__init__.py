#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.Helper.helper_functions import get_my_ip
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def generate_key():
    return "123456"

def save_mqtt_device(user, type, location, id, data, db):
    if not user.has_permission(location):
        return {'result': 'nopermission'}

    #if type == MQTT_SENSOR:
    #    Database.insert("INSERT INTO MQTT_SENSORS")

    item_data = json.loads(data)

    for item in item_data:
        if item['devicetype'] == "sensor":
            Database.insert("INSERT INTO MQTT_SENSORS (NAME, ICON, TYPE, ROOM, SAVE_DATA, DEVICE_ID, VALUE_ID, LAST_VALUE) VALUES (:name, :icon, :type, :room, :save_data, :dev_id, :val_id, \"N/A\")",
            {'name': item['name'], 'icon': item['icon'], 'type': item['sensor_type'],
            'room': location, 'save_data': item['save_data'], 'dev_id': id, 'val_id': item['id']}, db)
        
    return Status(type=STATUS_OK).get_dict()

def generate_device_data(user, location, db):
    if not user.has_permission(location):
        return {'result': 'nopermission'}

    item = Database.select_one("SELECT * FROM MQTT_DEVICES ORDER BY ID DESC", {}, db)

    if item is not None:
        new_id = item['ID']+1
    else:
        new_id = 0

    topic = "/home/device/"+str(new_id)

    key = generate_key()

    Database.insert("INSERT INTO MQTT_DEVICES (ID, LOCATION, KEY, TOPIC) VALUES (:id, :location, :key, :topic)",
                {'id': new_id, 'location': location, 'key': key, 'topic': topic}, db)

    return {'id': new_id, 'topic': topic, 'key': key, 'ip': get_my_ip(),
            'remoteid': Database.get_server_data("REMOTE_ID", db)}

def add_to_intermediates(id, db):
        Database.insert("INSERT INTO MQTT_DEVICE_INTERMEDIATES (ID) VALUES (:id)", {'id': id})

def is_in_intermediates(id, db):
        data = Database.select_one("SELECT COUNT(*) FROM MQTT_DEVICE_INTERMEDIATES WHERE ID = :id", {'id': id}, db)

        if data['COUNT(*)'] == 0:
            return False
        else:
            return True
