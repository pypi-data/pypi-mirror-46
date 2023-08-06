#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from Homevee.DeviceAPI import blind_control
from Homevee.DeviceAPI.heating import heating_control
from Homevee.DeviceAPI.rgb_control import rgb_control
from Homevee.DeviceAPI.set_modes import set_modes
from Homevee.DeviceAPI.wake_on_lan import wake_on_lan, wake_xbox_on_lan
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database
from Homevee.Utils.DeviceTypes import *
from Homevee.Utils.NotificationManager import NotificationManager


def run_scene(user, id, db):

        cur = db.cursor()

        Database.select_all("SELECT * FROM SCENES WHERE ID = :id",
                    {'id': id})

        result = cur.fetchone()

        if (result is None):
            return None

        id = result['ID']

        action_data = result['ACTION_DATA']

        action_data = json.loads(action_data)

        # run actions
        run_actions(action_data, db)

        return Status(type=STATUS_OK).get_dict()


def run_actions(action_data, db):
    for action in action_data:
        if action['type'] == "push_notification":
            msg = action['message']
            users = action['users']
            NotificationManager().send_notification_to_users(users, "Homevee", msg, db)
        elif action['type'] == "run_scene":
            scene_id = action['id']
            run_scene(None, scene_id, db)
        elif action['type'] == 'control_device':
            device_type = action['devicetype']
            device_id = action['id']

            if device_type in [FUNKSTECKDOSE, URL_TOGGLE, URL_SWITCH, ZWAVE_SWITCH]:
                set_modes(None, device_type, device_id, action['value'], db, False)
            elif device_type == WAKE_ON_LAN:
                wake_on_lan(None, device_id, db, False)
            elif device_type == XBOX_ONE_WOL:
                wake_xbox_on_lan(None, device_id, db, False)
            elif device_type in [ZWAVE_THERMOSTAT, MAX_THERMOSTAT, RADEMACHER_THERMOSTAT]:
                heating_control(None, device_type, device_id, action['value'], db, False)
            elif device_type in [RADEMACHER_BLIND_CONTROL]:
                blind_control.set_blinds(None, device_type, device_id, action['value'], db, False)
            elif device_type in [PHILIPS_HUE_LIGHT, URL_RGB_LIGHT]:
                data = json.loads(action['value'])
                rgb_control(None, device_type, device_id, data['mode'], data['brightness'], data['color'], db, False)