import os

from Homevee.DeviceAPI import xbox_wol
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def wake_on_lan(user, id, db, check_user=True):
    device = Database.select_all("SELECT * FROM WAKE_ON_LAN WHERE DEVICE == :id", {'id': id}, db)
    if check_user and not user.has_permission(device['LOCATION']):
        return {'result': 'nopermission'}

    os.system("sudo wakeonlan "+device['MAC_ADDRESS'])

    return Status(type=STATUS_OK).get_dict()

def get_wol_devices(user, room, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    devices = []

    results = Database.select_all("SELECT * FROM WAKE_ON_LAN WHERE LOCATION == :room", {'room': room}, db)

    for data in results:
        devices.append({'name': data['NAME'], 'id': data['DEVICE'], 'icon': data['ICON']})

    return {'devices': devices}

def wake_xbox_on_lan(user, id, db, check_user=True):
        device = Database.select_all("SELECT * FROM XBOX_ONE_WOL WHERE ID == :id",
                    {'id': id}, db)

        if check_user and not user.has_permission(device['LOCATION']):
            return {'result': 'nopermission'}

        ip = device['IP_ADDRESS']
        live_id = device['XBOX_LIVE_ID']

        xbox_wol.xbox_wake_up(ip, live_id)

        return Status(type=STATUS_OK).get_dict()

def get_xbox_devices(user, room, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    devices = []
    results = Database.select_all("SELECT * FROM XBOX_ONE_WOL WHERE LOCATION == :room", {'room': room}, db)

    for data in results:
        devices.append({'name': data['NAME'], 'id': data['ID'], 'icon': data['ICON']})

    return {'devices': devices}