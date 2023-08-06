#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from Homevee.Item.Event import Event
from Homevee.Utils.Database_NEW import Database

'''Gibt die Ereignisse zurück'''
def get_events(user, type, limit, offset, db: Database = None):
    if db is None:
        db = Database()
    events = Event.load_all_from_db_desc_date_by_type(offset, limit, type)
    user.events_last_checked = time.time()
    user.save_to_db(db)
    return {'events': Event.list_to_dict(events)}

'''Gibt die Anzahl der ungesehenen Ereignisse zurück'''
def get_unseen_events(user, db: Database = None):
    if db is None:
        db = Database()
    count = Event.get_unseen_events(user)
    return {'eventcount': count}

'''Gibt die vorhandenen Ereignis-Typen zurück'''
def get_event_types(db):
    results = db.select_all("SELECT DISTINCT TYPE FROM EVENTS ORDER BY TYPE", {})

    types = []

    for data in results:
        types.append(data['TYPE'])

    return {'types': types}

'''Erstellt ein neues Ereignis'''
def add_event(type, text, db: Database = None):
    if db is None:
        db = Database()
    event = Event(text=text, type=type)
    return event.save_to_db()