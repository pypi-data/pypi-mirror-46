#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Utils.Database import Database

def get_toggle_devices(username, room, db):
    devices = []
    results = Database.select_all("SELECT * FROM URL_TOGGLE WHERE LOCATION = :location",
                {'location': room}, db)

    for toggle in results:
        devices.append({'name': toggle['NAME'], 'id': toggle['ID'], 'type': 'URL-Toggle',
            'icon': toggle['ICON']})

    return {'toggles': devices}