#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.DeviceAPI.blind_control import get_blinds
from Homevee.DeviceAPI.dimmer import get_dimmers
from Homevee.DeviceAPI.energy_data import get_power_usage_devices
from Homevee.DeviceAPI.get_modes import get_modes
from Homevee.DeviceAPI.heating import get_thermostats
from Homevee.DeviceAPI.rgb_control import get_rgb_devices
from Homevee.DeviceAPI.toggle_devices import get_toggle_devices
from Homevee.DeviceAPI.wake_on_lan import get_xbox_devices, get_wol_devices
from Homevee.Functions.sensor_data import get_sensor_data
from Homevee.Functions.triggers import get_triggers
from Homevee.Helper import Logger
from Homevee.Item import Item
from Homevee.Item.Room import Room
from Homevee.Item.Status import *
from Homevee.Manager.scenes import get_scenes
from Homevee.Utils.DeviceTypes import *

CONTROL_TYPE_SWITCH = "switch"
CONTROL_TYPE_VALUE = "value"
CONTROL_TYPE_DIMMER = "dimmer"
CONTROL_TYPE_TOOGLE = "toggle"
CONTROL_TYPE_TRIGGER = "trigger"
CONTROL_TYPE_RGB = "rgb"
CONTROL_TYPE_HEATING = "heating"
CONTROL_TYPE_SCENES = "scenes"
CONTROL_TYPE_WOL = "wwakeonlan"
CONTROL_TYPE_XBOXONE = "xboxone"
CONTROL_TYPE_BLINDS = "blinds"

def get_rooms(user, db):
    rooms = []
    all_rooms = Room.load_all(db)
    for room in all_rooms:
        if(user.has_permission(room.id)):
            rooms.append(room)
    return {'rooms': Room.list_to_dict(rooms)}

def get_room_data(user, room, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    roomdata = []

    room = Item.load_from_db(Room, room, db)

    #Schalter abfragen
    switchdata = get_modes(user, room, "", "", db)
    for item in switchdata['modi']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype':item['device_type'],
            'icon': item['icon'], 'type': CONTROL_TYPE_SWITCH, 'value': item['mode']})

    #Dimmer
    dimmerdata = get_dimmers(user, room, db)
    for item in dimmerdata['dimmer']:
        roomdata.append({'name': item['name'], 'id': item['device'], 'devicetype': item['type'],
                         'icon': item['icon'], 'type': CONTROL_TYPE_DIMMER, 'value': item['value']})

    #Toggle
    toggledata = get_toggle_devices(user, room, db)
    for item in toggledata['toggles']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype':item['type'],
            'icon': item['icon'], 'type': CONTROL_TYPE_TOOGLE, 'value': ''})

    #Trigger
    triggerdata = get_triggers(user, room, db)
    for item in triggerdata['triggers']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype':item['type'],
            'icon': item['icon'], 'type': CONTROL_TYPE_TRIGGER, 'value': ''})

    #RGB
    rgbdata = get_rgb_devices(user, room, db)
    for item in rgbdata['rgb']:
        Logger.log(item)
        roomdata.append({'name': item['name'], 'devicetype':item['type'], 'id': item['id'],
            'icon': item['icon'], 'type': CONTROL_TYPE_RGB, 'value': item['value']})

    #Thermostate
    thermostat_data = get_thermostats(user, room, db)
    for item in thermostat_data['thermostats'][0]['thermostat_array']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': item['type'],
                         'icon': item['icon'], 'type': CONTROL_TYPE_HEATING, 'value': item['data']['value'],
                         'step': 0.5, 'min': item['data']['min'], 'max': item['data']['max']})

    #Sensoren abfragen
    sensordata = get_sensor_data(user, room, db)
    for item in sensordata['values'][0]['value_array']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': item['device_type'],
                         'icon': item['icon'], 'type': CONTROL_TYPE_VALUE, 'value': item['value']})

    #Szenen abfragen
    scenedata = get_scenes(user, room, db)
    if len(scenedata['scenes']) > 0:
        roomdata.append({'name': "Szenen", 'id': "scenes", 'devicetype': "scenes",
                         'icon': "scenes", 'type': CONTROL_TYPE_SCENES, 'value': ""})

    #WOL abfragen
    wol_devices = get_wol_devices(user, room, db)
    for item in wol_devices['devices']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': WAKE_ON_LAN,
                         'icon': item['icon'], 'type': CONTROL_TYPE_WOL})

    #XBOX ONE WOL abfragen
    xbox_devices = get_xbox_devices(user, room, db)
    for item in xbox_devices['devices']:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': XBOX_ONE_WOL,
                         'icon': item['icon'], 'type': CONTROL_TYPE_XBOXONE})

    #Jalousie-Steuerung
    blind_controls = get_blinds(user, room, db)['blinds']
    for item in blind_controls:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': item['type'],
                         'icon': item['icon'], 'type': CONTROL_TYPE_BLINDS, 'value': item['value']})

    #Strom-Messgeräte
    power_usage_devices = get_power_usage_devices(user, room, db)
    for item in power_usage_devices:
        roomdata.append({'name': item['name'], 'id': item['id'], 'devicetype': item['devicetype'],
                         'icon': item['icon'], 'type': CONTROL_TYPE_VALUE, 'value': item['value']})

    return {'roomdata': roomdata}

'''<?php
	
    //Neu dazugekommen
	$reeddata = getReedData($room, "", "", $db);
    foreach($reeddata['values'][0]['value_array'] as $reed){
		//Die Werte des Arrays wurden angepasst
        array_push($roomdata, array('name' => $reed['shortform'], 'device' => $reed['id'],
		'icon' => $reed['icon'], 'type' => "reed", 'device_type' => $reed['device_type'], 'value' => $reed['wert']));
    }
	
	$presencedata = getPresenceData($room, "", "", $db);
    foreach($presencedata['values'][0]['value_array'] as $presence){
        array_push($roomdata, array('name' => $presence['shortform'], 'device' => $presence['id'],
		'icon' => $presence['icon'], 'type' => "presence", 'device_type' => $presence['device_type'], 'value' => $presence['wert']));
    }
	
    $diydata = getDIYDevices($room, $db);
    foreach($diydata['diydevices'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['device'], 'icon' => $device['icon'],
		'type' => 'diydevice', 'value' => "", 'device_type' => "DIY Gerät"));
    }
	
    $dimmer = getDimmers($room, $db);
    foreach($dimmer['dimmers'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['id'], 'icon' => $device['icon'],
		'type' => 'dimmer', 'value' => $device['value'], 'device_type' => $device['device_type']));
    }
	
    $powermeters = getPowerMeterData($room, "", "", "", $db);
	
    foreach($powermeters['powermeters'][0]['value_array'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['id'], 'icon' => $device['icon'],
		'type' => 'powermeter', 'value' => $device['value'], 'device_type' => $device['device_type']));
    }
	
	//IP-Kameras abfragen
	$ipcameras = getIpCameraData($room, "", $db);
	
    foreach($ipcameras['ipcameras'][0]['value_array'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['id'], 'icon' => $device['icon'],
		'type' => 'ipcamera', 'value' => $device['value'], 'device_type' => $device['device_type'],
		'url' => $device['url'], 'username' => $device['username'], 'password' => $device['password']));
    }
	
    //Thermostate
	$thermostats = getHeatingData($room, "", "", "1", $db);
	
    foreach($thermostats['thermostats'][0]['thermostat_array'] as $thermostat){
        array_push($roomdata, array('name' => $thermostat['name'], 'device' => $thermostat['id'],
		'icon' => $thermostat['icon'], 'type' => "heating", 'device_type' => $thermostat['device_type'], 'value' => $thermostat['data']['value'],
		'einheit' => $thermostat['data']['einheit'], 'min' => $thermostat['data']['min'], 'max' => $thermostat['data']['max'], 'step' => 0.5));
    }
	
	//WOL-Geräte
	$devices = getWakeOnLanDevices($room, $db);
	
    foreach($devices['devices'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['id'],
		'icon' => $device['icon'], 'type' => "wakeonlan", 'device_type' => "Wake on Lan Gerät", 'value' => "Wake on Lan"));
    }
	
	//XBOX One
	$devices = getXboxOneDevices($room, $db);
	
    foreach($devices['devices'] as $device){
        array_push($roomdata, array('name' => $device['name'], 'device' => $device['id'],
		'icon' => $device['icon'], 'type' => "xboxone", 'device_type' => "XBOX One", 'value' => "Hochfahren"));
    }
     
    return array('roomdata' => $roomdata);
}
 
?>'''