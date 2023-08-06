#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.DeviceAPI.zwave.utils import do_zwave_request


def get_data(device_id, db):
    return do_zwave_request("/ZAutomation/api/v1/devices/"+device_id, db)

def set_binary_device(device_id, value, db):
    return do_zwave_request("/ZAutomation/api/v1/devices/"+device_id+"/command/"+value, db)

def set_multistate_device(device_id, value, db):
    return do_zwave_request("/ZAutomation/api/v1/devices/"+device_id+"/command/exact?level="+value, db)