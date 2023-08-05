#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Utils.Database import Database


def add_trigger(user, location, id, db):
    return

def get_triggers(user, room, db):
    if not user.has_permission(room):
        return {'result': 'nopermission'}

    triggers = []

    results = Database.select_all("SELECT * FROM MQTT_TRIGGERS WHERE LOCATION = :location", {'location': room}, db)

    for item in results:
        triggers.append({'name': item['NAME'], 'id': item['ID'], 'type': 'MQTT-Trigger', 'icon': item['ICON']})

    return {'triggers': triggers}