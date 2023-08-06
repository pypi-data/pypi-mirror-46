#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from Homevee.DeviceAPI import max_cube, zwave, philips_hue, rademacher_homepilot
from Homevee.Functions.room_data import get_rooms
from Homevee.Functions.sensor_data import SENSOR_TYPE_MAP
from Homevee.Helper import Logger
from Homevee.Item.Gateway import *
from Homevee.Item.Status import *
from Homevee.Utils.DeviceTypes import *


def get_gateway_devices(user, type, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    if type == Z_WAVE_GATEWAY:
        return zwave.get_devices.get_devices(db)
    if type == PHILIPS_HUE_BRIDGE:
        return philips_hue.get_devices(db)
    if type == RADEMACHER_HOMEPILOT:
        return rademacher_homepilot.get_devices(db)
    elif type == MAX_CUBE:
        gateway = Item.load_from_db(Gateway, MAX_CUBE, db)

        Logger.log(gateway.ip)

        devices = max_cube.get_devices(gateway.ip)

        if devices is not None:
            return {'devices': devices}
        else:
            return {'devices': []}
    elif type == "Network":
        network_devices = []

        hostnames = os.popen("arp -a").read()

        ip_adresses = os.popen("arp -a").read()

        Logger.log(hostnames)
        #print ip_adresses

        #for i in range(0, len(hostnames)):

        return {'devices': network_devices}
    else:
        return "nosuchgateway"

'''
function getGatewayDevices($type, $db){
	switch($type){
		case "Network":
			$networkDevices = array();

			exec("arp", $hostnames);
			exec("arp -n", $ipAdresses);

			for($i = 1; $i < sizeOf($hostnames); $i++){

				$names = preg_replace('!\s+!', ' ', $hostnames[$i]);

				$name = explode(" ", $names)[0];

				$adresses = preg_replace('!\s+!', ' ', $ipAdresses[$i]);

				$data = explode(" ", $adresses);

				$ip = $data[0];

				$mac = $data[2];

				array_push($networkDevices, array('id' => $ip, 'title' => $name, 'id2' => $mac));
			}

			return array('devices' => $networkDevices);
		default:
			return "nosuchgateway";
	}
}
'''

def add_edit_device(user, device_id, type, data, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    add_new = (device_id == None or device_id == "" or device_id == "-1")

    type = type.decode("utf-8")

    data_array = json.loads(data)



    #XBOX One WOL
    if type == XBOX_ONE_WOL:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'],
                       'ip': data_array['ip'], 'live_id': data_array['liveid']}

        if device_id == "-1" or device_id is -1:
            Database.insert(
                "INSERT OR IGNORE INTO 'XBOX_ONE_WOL' (LOCATION, ICON, NAME, IP_ADDRESS, XBOX_LIVE_ID) VALUES (:room, :icon, :name, :ip, :live_id);",
                param_array, db)
        else:

            param_array['id'] = device_id

            Database.update(
                "UPDATE OR IGNORE 'XBOX_ONE_WOL' SET LOCATION = :room, ICON = :icon, NAME = :name, IP_ADDRESS = :ip, XBOX_LIVE_ID = :live_id WHERE ID == :id;",
                param_array, db)

    # Philips Hue
    elif type == PHILIPS_HUE_LIGHT:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'], 'id': device_id}

        Database.insert(
            "INSERT OR IGNORE INTO 'PHILIPS_HUE_LIGHTS' (LOCATION, ID, ICON, NAME) VALUES (:room, :id, :icon, :name);",
            param_array, db)

        Database.update(
            "UPDATE OR IGNORE 'PHILIPS_HUE_LIGHTS' SET LOCATION = :room, ICON = :icon, NAME = :name WHERE ID == :id;",
            param_array, db)
    #MQTT Sensor
    elif type == MQTT_SENSOR:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data['icon'], 'id': device_id,
                       'key': data_array['key'], 'topic': data_array['topic'], 'save_data': data_array['save_data']}

        Database.insert(
            "INSERT OR IGNORE INTO 'MQTT_SENSORS' (ROOM, ID, ICON, NAME, KEY, TOPIC, SAVE_DATA) VALUES (:room, :id, :icon, :name, :key, :topic, :save_data);",
            param_array, db)

        Database.update(
            "UPDATE OR IGNORE 'MQTT_SENSORS' SET ROOM = :room, ICON = :icon, NAME = :name, KEY = :key, TOPIC = :topic, SAVE_DATA = :save_data, WHERE ID == :id;",
            param_array, db)

    #433 MHz
    elif type == FUNKSTECKDOSE:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'],
                       'hauscode': data_array['hauscode'], 'nummer': data_array['steckdosennummer']}

        '''if add_new:
                        data = Database.select_one("SELECT COUNT(*) FROM 'funksteckdosen' WHERE HAUSCODE = :hauscode AND STECKDOSENNUMMER = :nummer;",
                                    {'hauscode': data_array['hauscode'], 'nummer': data_array['steckdosennummer']})

                        count = cur.fetchone()['COUNT(*)']

                        if(int(count) != 0):
                            return "hauscodesocketnumberinuse"
                    else:
                        param_array['id'] = device_id'''

        if add_new:
            Database.insert("INSERT INTO 'funksteckdosen' (ROOM, HAUSCODE, STECKDOSENNUMMER, ICON, NAME) VALUES (:room, :hauscode, :nummer, :icon, :name);",
                        param_array, db)
        else:
            param_array['id'] = device_id

            Database.update("UPDATE 'funksteckdosen' SET ROOM = :room, HAUSCODE = :hauscode, STECKDOSENNUMMER = :nummer, ICON = :icon, NAME = :name WHERE DEVICE == :id;",
                        param_array, db)
    # MAX!
    elif type == MAX_THERMOSTAT:
        param_array = {'room': data_array['room'], 'name': data_array['name'],
                       'icon': data_array['icon'], 'id': device_id}

        Database.update("UPDATE OR IGNORE 'MAX_THERMOSTATS' SET RAUM = :room, NAME = :name, ICON = :icon WHERE ID = :id;",
            param_array, db)

        Database.insert("INSERT OR IGNORE INTO 'MAX_THERMOSTATS' (RAUM, ID, NAME, ICON) VALUES (:room, :id, :name, :icon);",
            param_array, db)
    # Rademacher!
    elif type == RADEMACHER_THERMOSTAT:
        param_array = {'room': data_array['room'], 'name': data_array['name'],
                       'icon': data_array['icon'], 'id': device_id}

        Database.update("UPDATE OR IGNORE 'HOMEPILOT_THERMOSTATS' SET ROOM = :room, NAME = :name, ICON = :icon WHERE ID = :id;",
            param_array, db)

        Database.insert("INSERT OR IGNORE INTO 'HOMEPILOT_THERMOSTATS' (ROOM, ID, NAME, ICON) VALUES (:room, :id, :name, :icon);",
            param_array, db)
    elif type == RADEMACHER_BLIND_CONTROL:
        param_array = {'room': data_array['room'], 'name': data_array['name'],
                       'icon': data_array['icon'], 'id': device_id}

        Database.update("UPDATE OR IGNORE 'HOMEPILOT_BLIND_CONTROL' SET LOCATION = :room, NAME = :name, ICON = :icon WHERE ID = :id;",
            param_array, db)

        Database.insert("INSERT OR IGNORE INTO 'HOMEPILOT_BLIND_CONTROL' (LOCATION, ID, NAME, ICON) VALUES (:room, :id, :name, :icon);",
            param_array, db)

    #Z-Wave
    elif type == ZWAVE_SENSOR:
        param_array = {'room': data_array['room'], 'savedata': data_array['savedata'], 'shortform': data_array['name'],
                       'sensor_type': data_array['sensor_type'], 'icon': data_array['icon'], 'id': device_id}

        count = Database.select_one("SELECT COUNT(*) FROM ZWAVE_SENSOREN WHERE ID = :id", {'id': device_id}, db)
        add_new = (count['COUNT(*)'] == 0)

        if add_new:
            Database.insert("INSERT INTO 'ZWAVE_SENSOREN' (RAUM, ID, SHORTFORM, ICON, SAVE_DATA, SENSOR_TYPE) VALUES (:room, :id, :shortform, :icon, :savedata, :sensor_type);",
                        param_array, db)
        else:
            Database.update("UPDATE 'ZWAVE_SENSOREN' SET RAUM = :room, SHORTFORM = :shortform, ICON = :icon, SAVE_DATA = :savedata, SENSOR_TYPE = :sensor_type WHERE ID = :id;",
                        param_array, db)
    elif type == ZWAVE_THERMOSTAT:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'], 'id': device_id}

        count = Database.select_one("SELECT COUNT(*) FROM ZWAVE_THERMOSTATS WHERE THERMOSTAT_ID = :id", {'id': device_id}, db)
        add_new = (count['COUNT(*)'] == 0)

        if add_new:
            Database.insert("INSERT INTO 'ZWAVE_THERMOSTATS' (RAUM, NAME, THERMOSTAT_ID, ICON) VALUES (:room,:name,:id,:icon);",
            param_array, db)
        else:
            Database.update("UPDATE 'ZWAVE_THERMOSTATS' SET RAUM = :room, NAME = :name, THERMOSTAT_ID = :id, ICON =:icon WHERE THERMOSTAT_ID = :id;",
            param_array, db)
    elif type == ZWAVE_POWER_METER:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'], 'id': device_id, 'daily_reset': data_array['is_reset_daily']}

        count = Database.select_one("SELECT COUNT(*) FROM ZWAVE_POWER_METER WHERE DEVICE_ID = :id", {'id': device_id}, db)
        add_new = (count['COUNT(*)'] == 0)

        if add_new:
            Database.insert("INSERT INTO 'ZWAVE_POWER_METER' (ROOM_ID, DEVICE_ID, DEVICE_NAME, ICON, IS_RESET_DAILY) VALUES (:room,:id,:name,:icon,:daily_reset);",
            param_array, db)
        else:
            Database.update("UPDATE 'ZWAVE_POWER_METER' SET ROOM_ID = :room, DEVICE_NAME = :name, DEVICE_ID = :id, ICON =:icon, IS_RESET_DAILY = :daily_reset WHERE DEVICE_ID =:id;",
            param_array, db)
    elif type == ZWAVE_SWITCH:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'], 'id': device_id}

        count = Database.select_one("SELECT COUNT(*) FROM ZWAVE_SWITCHES WHERE ID = :id", {'id': device_id}, db)
        add_new = (count['COUNT(*)'] == 0)

        if add_new:
            Database.insert("INSERT INTO 'ZWAVE_SWITCHES' (LOCATION, NAME, ID, ICON) VALUES (:room,:name,:id,:icon);",
            param_array, db)
        else:
            Database.update("UPDATE 'ZWAVE_SWITCHES' SET LOCATION = :room, NAME = :name, ID = :id, ICON =:icon WHERE ID =:id;",
            param_array, db)
    elif type == ZWAVE_DIMMER:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'icon': data_array['icon'], 'id': device_id}

        count = Database.select_one("SELECT COUNT(*) FROM ZWAVE_DIMMER WHERE ID = :id", {'id': device_id}, db)
        add_new = (count['COUNT(*)'] == 0)

        if add_new:
            Database.insert("INSERT INTO 'ZWAVE_DIMMER' (LOCATION, NAME, ID, ICON) VALUES (:room,:name,:id,:icon);",
            param_array, db)
        else:
            Database.update("UPDATE 'ZWAVE_DIMMER' SET LOCATION = :room, NAME = :name, ID = :id, ICON =:icon WHERE ID =:id;",
            param_array, db)
    #Media Center
    elif type == MEDIA_CENTER:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'ip': data_array['ip'],
                       'username': data_array['username'], 'password': data_array['password'], 'type': data_array['type']}

        if add_new:
            Database.insert("INSERT INTO 'MEDIA_CENTER' (LOCATION, NAME, IP, USERNAME, PASSWORD, TYPE) VALUES (:room,:name, :ip, :username, :password, :type);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'MEDIA_CENTER' SET LOCATION = :room, NAME = :name, IP = :id, USERNAME = :username, PASSWORD = :password, TYPE = :type, ICON =:icon WHERE ID = :id;",
            param_array, db)
    #URL-Devices
    elif type == URL_SWITCH:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'on': data_array['onurl'],
                       'off': data_array['offurl'], 'val': data_array['valurl'], 'icon': data_array['icon']}

        if add_new:
            Database.insert("INSERT INTO 'URL_SWITCH_BINARY' (LOCATION, NAME, URL_ON, URL_OFF, URL_GET_STATE, ICON) VALUES (:room,:name, :on, :off, :val, :icon);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'URL_SWITCH_BINARY' SET LOCATION = :room, NAME = :name, URL_ON = :on, URL_OFF = :off, URL_GET_STATE = :val, ICON =:icon WHERE ID = :id;",
            param_array, db)
    elif type == URL_TOGGLE:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'toggle': data_array['toggleurl'],
                       'icon': data_array['icon']}

        if add_new:
            Database.insert("INSERT INTO 'URL_TOGGLE' (LOCATION, NAME, TOGGLE_URL, ICON) VALUES (:room, :name, :toggle, :icon);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'URL_TOGGLE' SET LOCATION = :room, NAME = :name, TOGGLE_URL = :toggle, ICON =:icon WHERE ID = :id;",
            param_array, db)
    elif type == URL_RGB_LIGHT:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'url': data_array['url'],
                       'icon': data_array['icon']}

        if add_new:
            Database.insert("INSERT INTO 'URL_RGB_LIGHT' (LOCATION, NAME, URL, ICON) VALUES (:room, :name, :url, :icon);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'URL_RGB_LIGHT' SET LOCATION = :room, NAME = :name, URL = :toggle, ICON =:icon WHERE ID = :id;",
            param_array, db)
    #MQTT
    elif type == MQTT_TRIGGER:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'topic': data_array['topic'],
                       'icon': data_array['icon'], 'type': data_array['type']}

        if add_new:
            Database.insert("INSERT INTO 'MQTT_TRIGGERS' (LOCATION, NAME, TOPIC, TYPE, ICON) VALUES (:room, :name, :topic, :type, :icon);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'MQTT_TRIGGERS' SET LOCATION = :room, NAME = :name, TOPIC = :topic, ICON =:icon WHERE ID = :id;",
            param_array, db)
    elif type == MQTT_SENSOR:
        param_array = {'room': data_array['room'], 'name': data_array['name'], 'topic': data_array['topic'],
                       'icon': data_array['icon'], 'type': data_array['type']}

        if add_new:
            Database.insert("INSERT INTO 'MQTT_SENSORS' (LOCATION, NAME, TOPIC, TYPE, ICON) VALUES (:room, :name, :topic, :type, :icon);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'MQTT_SENSORS' SET LOCATION = :room, NAME = :name, TOPIC = :topic, ICON =:icon WHERE ID = :id;",
            param_array, db)
    #Wake on Lan
    elif type == WAKE_ON_LAN:
        param_array = {'room': data_array['room'], 'name': data_array['name'],
                       'icon': data_array['icon'], 'mac': data_array['mac']}

        if add_new:
            Database.insert("INSERT INTO 'WAKE_ON_LAN' (LOCATION, NAME, ICON, MAC_ADDRESS) VALUES (:room, :name, :icon, :mac);",
            param_array, db)
        else:
            param_array['id'] = device_id
            Database.update("UPDATE 'WAKE_ON_LAN' SET LOCATION = :room, NAME = :name, MAC_ADDRESS = :mac, ICON =:icon WHERE DEVICE = :id;",
            param_array, db)
    else:
        return {'result': 'nosuchtype'}

    return Status(type=STATUS_OK).get_dict()

def delete_device(user, type, id, db):
    #type = type.encode('utf-8')
    db_cols = {
        FUNKSTECKDOSE: {'table': 'FUNKSTECKDOSEN', 'location': 'ROOM', 'id': 'DEVICE'},
        PHILIPS_HUE_LIGHT: {'table': 'PHILIPS_HUE_LIGHTS', 'location': 'LOCATION', 'id': 'ID'},
        WAKE_ON_LAN: {'table': 'WAKE_ON_LAN', 'location': 'LOCATION', 'id': 'DEVICE'},
        XBOX_ONE_WOL: {'table': 'XBOX_ONE_WOL', 'location': 'LOCATION', 'id': 'ID'},
        URL_RGB_LIGHT: {'table': 'URL_RGB_LIGHT', 'location': 'LOCATION', 'id': 'ID'},
        MQTT_SENSOR: {'table': 'MQTT_SENSORS', 'location': 'ROOM', 'id': 'ID'},
        URL_TOGGLE: {'table': 'URL_TOGGLE', 'location': 'LOCATION', 'id': 'ID'},
        URL_SWITCH: {'table': 'URL_SWITCH', 'location': 'LOCATION', 'id': 'ID'},
        ZWAVE_DIMMER: {'table': 'ZWAVE_DIMMER', 'location': 'LOCATION', 'id': 'ID'},
        ZWAVE_SWITCH: {'table': 'ZWAVE_SWITCHES', 'location': 'LOCATION', 'id': 'ID'},
        ZWAVE_SENSOR: {'table': 'ZWAVE_SENSOREN', 'location': 'RAUM', 'id': 'ID'},
        ZWAVE_POWER_METER: {'table': 'ZWAVE_POWER_METER', 'location': 'ROOM_ID', 'id': 'DEVICE_ID'},
        ZWAVE_THERMOSTAT: {'table': 'ZWAVE_THERMOSTATS', 'location': 'RAUM', 'id': 'THERMOSTAT_ID'},
        MAX_THERMOSTAT: {'table': 'MAX_THERMOSTATS', 'location': 'RAUM', 'id': 'ID'},
        RADEMACHER_THERMOSTAT: {'table': 'HOMEPILOT_THERMOSTATS', 'location': 'ROOM', 'id': 'ID'},
        RADEMACHER_BLIND_CONTROL: {'table': 'HOMEPILOT_BLIND_CONTROL', 'location': 'LOCATION', 'id': 'ID'}
    }

    if type not in db_cols:
        return {'result': 'nosuchtype'}

    data = Database.select_one("SELECT * FROM "+db_cols[type]['table']+" WHERE "+db_cols[type]['id']+" = :id",
                {'id': id}, db)

    Logger.log(data)

    if not user.has_permission(data[db_cols[type]['location']]):
        return {'result': 'nopermission'}

    Database.delete("DELETE FROM "+db_cols[type]['table']+" WHERE " + db_cols[type]['id'] + " = :id",
                {'id': id})

    return Status(type=STATUS_OK).get_dict()

def get_device_data(user, type, id, db):
    if not user.has_permission("admin"):
        return {'result': 'noadmin'}

    room_array = {}

    for room in get_rooms(user, db)['rooms']:
        room_array[room['location']] = room['name']

    Logger.log(room_array)

    param_array = {'id': id}

    device_data = {}

    #Funksteckdose
    if type == FUNKSTECKDOSE:
        data = Database.select_one("SELECT * FROM FUNKSTECKDOSEN WHERE DEVICE = :id", param_array, db)

        device_data = {'room': room_array[int(data['ROOM'])], 'location': data['ROOM'], 'name': data['NAME'],
                       'hauscode': data['HAUSCODE'], 'icon': data['ICON'], 'steckdosennummer': data['STECKDOSENNUMMER']}
    #Z-Wave
    elif type == ZWAVE_POWER_METER:
        data = Database.select_one("SELECT * FROM ZWAVE_POWER_METER WHERE DEVICE_ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['ROOM_ID'])], 'location': data['ROOM_ID'], 'name': data['DEVICE_NAME'],
                       'is_reset_daily': (data['IS_RESET_DAILY']==1), 'icon': data['ICON']}
    elif type == ZWAVE_SENSOR:
        data = Database.select_one("SELECT * FROM ZWAVE_SENSOREN WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['RAUM'])], 'location': data['RAUM'], 'name': data['SHORTFORM'],
                       'save_data': data['SAVE_DATA'], 'icon': data['ICON'],
                       'sensor_type': data['SENSOR_TYPE'], 'sensor_type_name': SENSOR_TYPE_MAP[data['SENSOR_TYPE']]['name']}
    elif type == ZWAVE_THERMOSTAT:
        data = Database.select_one("SELECT * FROM ZWAVE_THERMOSTATS WHERE THERMOSTAT_ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['RAUM'])], 'location': data['RAUM'], 'name': data['NAME'],
                       'icon': data['ICON']}
    elif type == ZWAVE_SWITCH:
        data = Database.select_one("SELECT * FROM ZWAVE_SWITCHES WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON']}
    elif type == ZWAVE_DIMMER:
        data = Database.select_one("SELECT * FROM ZWAVE_DIMMER WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON']}
    #MQTT-Sensor
    elif type == MQTT_SENSOR:
        data = Database.select_one("SELECT * FROM MQTT_SENSORS, MQTT_DEVICES WHERE MQTT_SENSORS.DEVICE_ID = MQTT_DEVICES.ID AND MQTT_SENSORS.ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['ROOM'])], 'location': data['ROOM'], 'name': data['NAME'], 'icon': data['ICON'],
                       'topic': data['TOPIC'], 'key': data['KEY'], 'sensor_type': data['TYPE'],
                       'sensor_type_name': SENSOR_TYPE_MAP[data['TYPE']]['name'], 'save_data': data['SAVE_DATA']==1}
    #IP Kamera
    elif type == IP_CAM:
        data = Database.select_one("SELECT * FROM ZWAVE_DIMMER WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'ip': data['IP'], 'port': data['PORT'], 'path': data['PATH'],
                       'username': data['USERNAME'], 'password': data['PASSWORD'], 'recordfootage': data['RECORD_FOOTAGE'],
                       'autodelete': data['AUTO_DELETE'], 'detectionthreshold': data['MOTION_DETECTION_THRESHOLD']}
    #URL-Toggle
    elif type == URL_TOGGLE:
        data = Database.select_one("SELECT * FROM URL_TOGGLE WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'toggle_url': data['TOGGLE_URL']}
    #URL-Switch
    elif type == URL_SWITCH:
        data = Database.select_one("SELECT * FROM URL_SWITCH_BINARY WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'on_url': data['URL_ON'], 'off_url': data['URL_OFF'],
                       'get_state_url': data['URL_GET_STATE']}
    #URL RGB-Licht
    elif type == URL_RGB_LIGHT:
        data = Database.select_one("SELECT * FROM URL_RGB_LIGHT WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'url': data['URL']}
    #Philips Hue RGB-Licht
    elif type == PHILIPS_HUE_LIGHT:
        data = Database.select_one("SELECT * FROM PHILIPS_HUE_LIGHTS WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'type': data['TYPE']}
    #MAX Thermostat
    elif type == MAX_THERMOSTAT:
        data = Database.select_one("SELECT * FROM MAX_THERMOSTATS WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['RAUM'])], 'location': data['RAUM'], 'name': data['NAME'],
                       'icon': data['ICON']}
    #Wake on Lan
    elif type == WAKE_ON_LAN:
        data = Database.select_one("SELECT * FROM WAKE_ON_LAN WHERE DEVICE = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'mac': data['MAC_ADDRESS']}
    #XBOX Wake on Lan
    elif type == XBOX_ONE_WOL:
        data = Database.select_one("SELECT * FROM XBOX_ONE_WOL WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON'], 'ip': data['IP_ADDRESS'], 'liveid': data['XBOX_LIVE_ID']}
    #Rademacher
    elif type == RADEMACHER_THERMOSTAT:
        data = Database.select_one("SELECT * FROM HOMEPILOT_THERMOSTATS WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['ROOM'])], 'location': data['ROOM'], 'name': data['NAME'],
                       'icon': data['ICON']}
    elif type == RADEMACHER_BLIND_CONTROL:
        data = Database.select_one("SELECT * FROM HOMEPILOT_BLIND_CONTROL WHERE ID = :id", param_array, db)

        device_data = {'room': room_array[int(data['LOCATION'])], 'location': data['LOCATION'], 'name': data['NAME'],
                       'icon': data['ICON']}
    else:
        return {'result': 'nosuchtype'}

    return {'devicedata': device_data}