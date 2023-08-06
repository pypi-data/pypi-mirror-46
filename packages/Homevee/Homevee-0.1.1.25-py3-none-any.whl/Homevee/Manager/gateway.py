#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests

from Homevee.Item.Gateway import *
from Homevee.Item.Status import *


def add_edit_gateway(username, type, user, password, change_pw, ip, port, gateway_type, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    param_array = {'name': type, 'ip': ip, 'port': port, 'key1': user, 'type': gateway_type}

    if change_pw == "true":
        param_array['key2'] = password

        db.update("UPDATE OR IGNORE 'GATEWAYS' SET IP = :ip, PORT = :port, KEY1 = :key1, KEY2 = :key2 TYPE = :type, WHERE NAME = :name;",
                    param_array)

        db.insert("INSERT OR IGNORE INTO 'GATEWAYS' (NAME, IP, PORT, KEY1, KEY2, TYPE) VALUES (:name, :ip, :port, :key1, :key2, :type);",
                    param_array)
    else:
        db.update("UPDATE OR IGNORE 'GATEWAYS' SET IP = :ip, PORT = :port, KEY1 = :key1 WHERE NAME = :name;",
                    param_array)

        db.insert("INSERT OR IGNORE INTO 'GATEWAYS' (NAME, IP, PORT, KEY1, TYPE) VALUES (:name, :ip, :port, :key1, :type);",
                    param_array)

    return Status(type=STATUS_OK).get_dict()

def delete_gateway(user, key, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    gateway = Item.load_from_db(Gateway, key)

    try:
        if(gateway.delete()):
            return Status(type=STATUS_OK).get_dict()
    except:
            return Status(type=STATUS_ERROR).get_dict()

    '''
    with db:
        cur = db.cursor()
        db.delete("DELETE FROM GATEWAYS WHERE NAME == :key", {'key': key})

        cur.close()

        #Abfrage erfolgreich?
        if True:
            return Status(type=STATUS_OK).get_dict()
        else:
            return Status(type=STATUS_ERROR).get_dict()
    '''

def get_gateways(user, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    results = db.select_all("SELECT * FROM GATEWAYS", {})

    gateways = []

    for gateway in results:
        gateways.append({'name': gateway['NAME'], 'ip': gateway['IP'], 'port': gateway['PORT'],
                            'key1': gateway['KEY1'], 'type': gateway['TYPE']})

    return {'gateways': gateways, 'gatewaytypesleft': get_gateway_types(user, db)}

def get_gateway_types(user, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    gateway_types = [
        {'key': Z_WAVE_GATEWAY, 'type': 'user'},
        {'key': FUNKSTECKDOSEN_CONTROLLER, 'type': 'url'},
        {'key': MAX_CUBE, 'type': 'url'},
        {'key': MQTT_BROKER, 'type': 'user'},
        {'key': PHILIPS_HUE_BRIDGE, 'type': 'apikey'},
        {'key': MIYO_CUBE, 'type': 'apikey'},
        {'key': RADEMACHER_HOMEPILOT, 'type': 'url'},
    ]

    results = db.select_all("SELECT NAME FROM GATEWAYS")

    for gateway in results:
        name = gateway['NAME']
        for i in range(0, len(gateway_types)-1):
            if gateway_types[i]['key'] == name:
                del gateway_types[i]

    return gateway_types

def connect_gateway(user, type, ip, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission("admin"):
        return {'result': 'noadmin'}

    if type == PHILIPS_HUE_BRIDGE:
        while True:
            #print("try connecting...")

            data = {"devicetype": "Homevee#system"}

            response = requests.post("http://" + ip + "/api", data=json.dumps(data))

            result = response.text

            #print("result: "+result)

            result = json.loads(result)

            result = result[0]

            if "error" in result:
                if result['error']['type'] == 101:
                    return {'result': 'error', 'msg': 'Drücke bitte die Taste auf deinem Philips Hue Gateway.'}
            elif "success" in result:
                user = result['success']['username']

                add_edit_gateway(user.username, type, user, "", "", ip, "80", "apikey", db)

                return Status(type=STATUS_OK).get_dict()
    elif type == MIYO_CUBE:
        while True:
            #print("try connecting...")

            response = requests.get("http://" + ip + "/api/link")

            result = response.text

            #print("result: "+result)

            result = json.loads(result)

            if "error" in result:
                if result['errorLoc'] == "NOTIFY_ERROR_LINKINACTIVE":
                    return {'result': 'error', 'msg': 'Drücke bitte die Taste hinten auf deinem MIYO Cube.'}
            elif "success" in result:
                user = result['success']['username']

                add_edit_gateway(user.username, type, user, "", "", ip, "80", "apikey", db)

                return Status(type=STATUS_OK).get_dict()
    else:
        return Status(type=STATUS_ERROR).get_dict()