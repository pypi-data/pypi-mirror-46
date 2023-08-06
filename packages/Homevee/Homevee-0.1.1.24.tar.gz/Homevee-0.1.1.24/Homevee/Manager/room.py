#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item import Item
from Homevee.Item.Room import Room
from Homevee.Item.Status import *
from Homevee.Manager.scenes import get_scenes
from Homevee.Utils.Database import Database


def add_edit_room(user, room_name, room_key, icon, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    try:
        room = Item.load_from_db(Room, room_key, db)
        room.name = room_name
        room.icon = icon
    except:
        room = Room(room_name, room_key)

    return room.api_save()

def delete_room(user, room_key, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    room = Item.load_from_db(Room, room_key, db)

    roomdata = room.get_room_data(db)

    #roomdata = get_room_data(user, room_key, db)['roomdata']

    if roomdata is not None and len(roomdata) == 1:
        if roomdata[0]['type'] == "scenes":
            scenes = get_scenes(user, room_key, db)

            for scene in scenes['scenes']:
                if scene['room'] == room_key:
                    return Status(type=STATUS_ROOM_HAS_ITEMS).get_dict()
    elif roomdata is not None and len(roomdata) > 1:
        return Status(type=STATUS_ROOM_HAS_ITEMS).get_dict()

    return room.api_delete()

def move_items_and_delete_old_room(user, old_room, new_room, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    params = {'oldroom': old_room, 'newroom': new_room}

    query_array = []

    #Funksteckdosen
    query_array.append("UPDATE 'funksteckdosen' SET ROOM = :newroom WHERE ROOM == :oldroom;")

    #Z-Wave
    query_array.append("UPDATE 'ZWAVE_SENSOREN' SET RAUM = :newroom WHERE RAUM == :oldroom;")
    query_array.append("UPDATE 'ZWAVE_THERMOSTATS' SET RAUM = :newroom WHERE RAUM == :oldroom;")

    #DIY
    query_array.append("UPDATE 'DIY_DEVICES' SET ROOM = :newroom WHERE ROOM == :oldroom;")
    query_array.append("UPDATE 'DIY_SENSORS' SET RAUM = :newroom WHERE RAUM == :oldroom;")
    query_array.append("UPDATE 'DIY_REEDSENSORS' SET RAUM = :newroom WHERE RAUM == :oldroom;")
    query_array.append("UPDATE 'DIY_SWITCHES' SET RAUM = :newroom WHERE RAUM == :oldroom;")

    #Szenen
    query_array.append("UPDATE 'SCENES' SET ROOM = :newroom WHERE ROOM == :oldroom;")


    for query in query_array:
        Database.update(query, params, db)

    return delete_room(user, old_room, db)

def delete_room_with_items(user, room_key, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    params = {'oldroom': room_key}

    query_array = []

    # Funksteckdosen
    query_array.append("DELETE FROM 'funksteckdosen' WHERE ROOM == :oldroom;")

    # Z-Wave
    query_array.append("DELETE FROM 'ZWAVE_SENSOREN' WHERE RAUM == :oldroom;")
    query_array.append("DELETE FROM 'ZWAVE_THERMOSTATS' WHERE RAUM == :oldroom;")

    # DIY
    query_array.append("DELETE FROM 'DIY_DEVICES' WHERE ROOM == :oldroom;")
    query_array.append("DELETE FROM 'DIY_REEDSENSORS' WHERE RAUM == :oldroom;")
    query_array.append("DELETE FROM 'DIY_SENSORS' WHERE RAUM == :oldroom;")
    query_array.append("DELETE FROM 'DIY_SWITCHES' WHERE RAUM == :oldroom;")

    # Szenen
    query_array.append("DELETE FROM 'SCENES' WHERE ROOM == :oldroom;")


    for query in query_array:
        Database.delete(query, params, db)

    return delete_room(user, room_key, db)