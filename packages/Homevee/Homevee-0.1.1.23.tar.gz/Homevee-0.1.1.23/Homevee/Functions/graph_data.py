#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from Homevee.Functions.sensor_data import get_einheit
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database

'''Gibt den Sensorwerteverlauf für den gewünschten Zeitraum zurück'''
def get_graph_data(user, room, type, id, von, bis, db):
    if not user.has_permission(room):
        return Status(type=STATUS_NO_PERMISSION).get_dict()

    if von == bis:
        datum = datetime.datetime.strptime(von, "%d.%m.%Y").strftime("%Y-%m-%d")

        return get_day_data(type, id, datum, db)
    else:
        return get_day_min_max(type, id, von, bis, db)

'''Gibt den Tageswerteverlauf des Sensors zurück'''
def get_day_data(type, id, datum, db):
    results = Database.select_all("""SELECT * FROM 'SENSOR_DATA' WHERE DEVICE_TYPE == :type AND DEVICE_ID == :id 
            AND DATETIME >= :start AND DATETIME < :ende AND VALUE != \"N/A\" ORDER BY DATETIME ASC""",
                {'type':type, 'id':id, 'start':datum+" 00:00", 'ende':datum+" 23:59"}, db)
    values = []

    for data in results:
        item = {'value':float(data['VALUE']), 'id':id, 'time':data['DATETIME'].replace(datum+" ","")}
        values.append(item)

    return {'values': values, 'einheit': get_einheit(type, id, db)}

'''Gibt die Höchst- & Tiefstwerte des angegebenen Datumsbereichs zurück'''
def get_day_min_max(type, id, von, bis, db):
    start = datetime.datetime.strptime(von, "%d.%m.%Y").strftime("%Y-%m-%d")
    ende = datetime.datetime.strptime(bis, "%d.%m.%Y").strftime("%Y-%m-%d")

    values = []

    results = Database.select_all("""SELECT MIN(VALUE) as MIN, MAX(VALUE) as MAX, strftime(\"%d.%m.%Y\", DATETIME) as FORMATTED_DATE
         FROM SENSOR_DATA WHERE DEVICE_TYPE == :type AND DEVICE_ID == :id AND DATETIME >= :start 
         AND DATETIME <= :ende AND VALUE != \"N/A\" GROUP BY DATETIME ORDER BY DATETIME ASC""",
        {'type': type, 'id': id, 'start': start+' 00:00', 'ende': ende+' 23:59'}, db)

    #print {'type': type, 'id': id, 'start': start, 'ende': ende}

    for data in results:
        item = {'date':data['FORMATTED_DATE'], 'min':data['MIN'], 'max':data['MAX']}

        values.append(item)

    return {'values':values, 'einheit': get_einheit(type, id, db)}