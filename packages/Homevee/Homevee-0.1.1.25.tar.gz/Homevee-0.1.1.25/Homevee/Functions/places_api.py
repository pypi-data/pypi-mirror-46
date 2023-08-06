#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Utils.Database_NEW import Database


def get_places(user, keyword, lat, lng, db: Database = None):
    if db is None:
        db = Database()
    places = []

    return places

def get_place_data(user, place_id, db: Database = None):
    if db is None:
        db = Database()
    data = {}

    return data