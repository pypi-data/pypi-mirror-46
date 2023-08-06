#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item.Room import Room
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_all_scenes(user, db):
    with db:
        cur = db.cursor()

        cur.execute("SELECT * FROM ROOMS")

        rooms = []

        for room in cur.fetchall():
            if not user.has_permission(room['LOCATION']):
                continue

            scenes = get_scenes(user, room['LOCATION'], db)

            scenes = scenes['scenes']

            if(len(scenes) is not 0):
                room_item = {'name': room['NAME'], 'location': room['LOCATION'], 'icon': room['ICON'], 'scenes': scenes}
                rooms.append(room_item)

        return {'rooms': rooms}

def get_scenes(user, location, db):
    scenes = []

    if isinstance(location, Room):
        location = location.id

    if user.has_permission(location):
        with db:
            cur = db.cursor()

            cur.execute("SELECT * FROM SCENES WHERE ROOM = :location",{'location': location})

            for item in cur.fetchall():
                scenes.append({'id': item['ID'], 'name': item['NAME'], 'action_data': item['ACTION_DATA'],
                              'location': item['ROOM']})

    return {'scenes': scenes}

def add_edit_scene(username, id, name, location, action_data, db):
    add_new = (id == None or id == "" or id == "-1")

    with db:
        cur = db.cursor()

        if(add_new):
            Database.insert("INSERT INTO SCENES (NAME, ROOM, ACTION_DATA) VALUES (:name, :room, :actions)",
                        {'name': name, 'room': location, 'actions': action_data})

            return Status(type=STATUS_OK).get_dict()

        else:
            Database.update("UPDATE SCENES SET NAME = :name, ROOM = :location, ACTION_DATA = :actions WHERE ID = :id",
                {'name': name, 'location': location, 'actions': action_data, 'id': id})

            return Status(type=STATUS_OK).get_dict()

def delete_scene(username, id, db):
    with db:
        cur = db.cursor()

        Database.delete("DELETE FROM SCENES WHERE ID = :id", {'id': id})

        return Status(type=STATUS_OK).get_dict()