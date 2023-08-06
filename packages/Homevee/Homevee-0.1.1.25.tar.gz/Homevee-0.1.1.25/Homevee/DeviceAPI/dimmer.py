#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.DeviceAPI import zwave
from Homevee.Item.Status import *
from Homevee.Utils.Database_NEW import Database
from Homevee.Utils.DeviceTypes import *

def get_dimmers(user, room, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    dimmer = []
    #Z-Wave Dimmer
    results = db.select_all("SELECT * FROM ZWAVE_DIMMER WHERE LOCATION == :room", {'room': room})

    for item in results:
        dimmer_item = {'device': item['ID'], 'value': item['VALUE'], 'icon': item['ICON'],
                     'name': item['NAME'], 'type': ZWAVE_DIMMER}
        dimmer.append(dimmer_item)

    return {'dimmer': dimmer}

def set_dimmer(user, type, id, value, db: Database = None):
    if db is None:
        db = Database()
    if type == ZWAVE_DIMMER:
        return set_zwave_dimmer(user, id, value, db)
    else:
        raise ValueError("Type does not exist")

def set_zwave_dimmer(user, id, value, db: Database = None):
    if db is None:
        db = Database()

        data = db.select_one("SELECT * FROM ZWAVE_DIMMER WHERE ID == :device",
                    {'device': id})

        if not user.has_permission(data['LOCATION']):
            return {'result': 'nopermission'}

        device_id = data['ID']

        result = zwave.device_control.set_multistate_device(device_id, value, db)

        if result['code'] == 200:
            db.update("UPDATE ZWAVE_DIMMER SET VALUE = :value WHERE ID = :id",
                        {'value': value, 'id': id})

            return {'result':'ok'}