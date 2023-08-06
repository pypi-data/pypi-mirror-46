#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.Item.Device import Device
from Homevee.Item.HeatingSchemeItem import HeatingSchemeItem
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def add_edit_heating_scheme_item(user, id, time, value, active, days, data, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    with db:
        cur = db.cursor()

        params = {'time': time, 'value': value, 'active': active}

        if id == "" or id is None:
            Database.insert("INSERT INTO HEATING_SCHEME (TIME, VALUE, ACTIVE) VALUES (:time, :value, :active)",
                        params)

            id = cur.lastrowid
        else:
            params['id'] = id
            Database.update("UPDATE HEATING_SCHEME SET TIME = :time, VALUE = :value, ACTIVE = :active WHERE ID = :id",
                params)

        #HEATING_SCHEME_DAYS bearbeiten
        Database.delete("DELETE FROM 'HEATING_SCHEME_DAYS' WHERE HEATING_SCHEME_ID = :id", {'id': id})

        day_array = json.loads(days)

        for day in day_array:
            Database.insert("INSERT INTO 'HEATING_SCHEME_DAYS' (HEATING_SCHEME_ID, WEEKDAY_ID) VALUES (:id, :weekday_id)",
                {'id': id, 'weekday_id': day})

        #HEATING_SCHEME_DEVICES bearbeiten
        Database.delete("DELETE FROM 'HEATING_SCHEME_DEVICES' WHERE ID = :id", {'id': id})

        device_array = json.loads(data)

        for device in device_array['devices']:
            Database.insert("INSERT INTO 'HEATING_SCHEME_DEVICES' (ID, LOCATION, TYPE, DEVICE_ID) VALUES (:id, :location, :type, :device_id)",
                {'id': id, 'location': device['location'], 'type': device['type'], 'device_id': device['id']})

        return Status(type=STATUS_OK).get_dict()

def delete_heating_scheme_item(user, id, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    heating_scheme_item = Device.load_from_db(HeatingSchemeItem, id)
    return heating_scheme_item.api_delete()

def get_heating_scheme_items(user, day, rooms, db):
    if not user.has_permission("admin"):
        return "noadmin"

    params = {'day': day}
    query_in_rooms_string = ""

    if rooms is not None and rooms != "":
        params['rooms'] = rooms
        query_in_rooms_string = "AND LOCATION IN (:rooms)"

    with db:
        cur = db.cursor()
        cur.execute("SELECT HEATING_SCHEME.ID, TIME, VALUE, ACTIVE, WEEKDAY_ID, ROOMS.NAME as LOCATION, TYPE, DEVICE_ID FROM HEATING_SCHEME, HEATING_SCHEME_DAYS, HEATING_SCHEME_DEVICES, ROOMS WHERE HEATING_SCHEME.ID = HEATING_SCHEME_DAYS.HEATING_SCHEME_ID AND HEATING_SCHEME.ID = HEATING_SCHEME_DEVICES.ID AND HEATING_SCHEME_DEVICES.LOCATION = ROOMS.LOCATION AND WEEKDAY_ID = :day "+query_in_rooms_string+" ORDER BY TIME",
                    params)

        heating_scheme_items = {}
        heating_scheme_data = {}

        results = cur.fetchall()

        for result in results:
            if result['ID'] not in heating_scheme_data:
                heating_scheme_data[result['ID']] = []

            heating_scheme_data[result['ID']].append({'location': result['LOCATION'], 'type': result['TYPE'], 'device':result['DEVICE_ID']})

            heating_scheme_items[result['ID']] = {'time': result['TIME'], 'value': result['VALUE'], 'isactive': (True if result['ACTIVE']=="true" else False)}

        for result in results:
            heating_scheme_items[result['ID']]['data'] = heating_scheme_data[result['ID']]

        cur.close()

        return {'heatingscheme': heating_scheme_items}

def get_heating_scheme_item_data(username, id, db):
    heating_scheme_item = {}

    params = {'id': id}


    with db:
        #Tage abfragen
        chosen_days = []
        cur = db.cursor()
        cur.execute("SELECT WEEKDAY_ID FROM HEATING_SCHEME_DAYS WHERE HEATING_SCHEME_ID == :id", params)
        for day in cur.fetchall():
            chosen_days.append(int(day['WEEKDAY_ID']))
        heating_scheme_item['days'] = chosen_days

        #Geräte abfragen
        devices = []
        results = Database.select_all("SELECT * FROM HEATING_SCHEME_DEVICES WHERE ID == :id", params, db)
        for device in results:
            devices.append({'id': device['DEVICE_ID'], 'type': device['TYPE'], 'location': device['LOCATION']})
        heating_scheme_item['devicearray'] = json.dumps({'devices': devices})

        #Daten
        cur.execute("SELECT * FROM HEATING_SCHEME WHERE ID == :id", params)
        scheme_item_data = cur.fetchone()

        heating_scheme_item['value'] = float(scheme_item_data['VALUE'])
        heating_scheme_item['time'] = scheme_item_data['TIME']
        heating_scheme_item['active'] = scheme_item_data['ACTIVE']

        return {'heatingschemeitem': heating_scheme_item}

def set_heating_scheme_item_active(user, id, active, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()
    try:
        Database.update("UPDATE HEATING_SCHEME SET ACTIVE = :active WHERE ID = :id", {'active': active, 'id': id})
        return Status(type=STATUS_OK).get_dict()
    except:
        pass
    return Status(type=STATUS_ERROR).get_dict()

def is_heating_scheme_active(user, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    is_active = Database.get_server_data("HEATING_SCHEME_ACTIVE", db)

    return {'isactive': is_active=="true"}

def set_heating_scheme_active(user, active, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    try:
        Database.set_server_data("HEATING_SCHEME_ACTIVE", active, db)
        return Status(type=STATUS_OK).get_dict()
    except:
        pass
    return Status(type=STATUS_ERROR).get_dict()