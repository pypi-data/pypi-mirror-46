#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_place(id, db):
    if(id is None or id == "" or id is -1):
        return None

    place = Database.select_one("SELECT * FROM PLACES WHERE ID = :id",
                {'id': id}, db)

    return place

def get_my_places(username, db):
    places = []

    results = Database.select_all("SELECT * FROM PLACES", {}, db)

    for place in results:
        places.append({'id': place['ID'], 'name': place['NAME'], 'address': place['ADDRESS'], 'latitude': place['LATITUDE'], 'longitude': place['LONGITUDE']})

    return {'places': places}

def add_edit_place(username, id, name, address, latitude, longitude, db):
    add_new = (id == None or id == "" or id == "-1")

    if (add_new):
        Database.insert("INSERT INTO PLACES (NAME, ADDRESS, LATITUDE, LONGITUDE) VALUES (:name, :address, :latitude, :longitude)",
                    {'name': name, 'address': address, 'latitude': latitude, 'longitude': longitude}, db)

        return Status(type=STATUS_OK).get_dict()

    else:
        Database.update("UPDATE SCENES SET NAME = :name, ADDRESS = :address, LATITUDE = :latitude, LONGITUDE = :longitude WHERE ID = :id",
                    {'name': name, 'address': address, 'latitude': latitude, 'longitude': longitude, 'id': id}, db)

        return Status(type=STATUS_OK).get_dict()

def delete_place(username, id, db):
    Database.delete("DELETE FROM PLACES WHERE ID = :id", {'id': id})
    return Status(type=STATUS_OK).get_dict()