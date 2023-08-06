#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Utils.Database_NEW import Database

def get_toggle_devices(username, room, db: Database = None):
    if db is None:
        db = Database()
    devices = []
    results = db.select_all("SELECT * FROM URL_TOGGLE WHERE LOCATION = :location",
                {'location': room})

    for toggle in results:
        devices.append({'name': toggle['NAME'], 'id': toggle['ID'], 'type': 'URL-Toggle',
            'icon': toggle['ICON']})

    return {'toggles': devices}