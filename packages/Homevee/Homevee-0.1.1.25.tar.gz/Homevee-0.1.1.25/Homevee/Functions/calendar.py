#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item import Item
from Homevee.Item.CalendarEntry import CalendarEntry
from Homevee.Utils.Database_NEW import Database


def get_calendar_item_dates(user, year, db: Database = None):
    if db is None:
        db = Database()
    return CalendarEntry.get_calendar_item_dates(year)

def get_calendar_day_items(user, date, db: Database = None):
    if db is None:
        db = Database()
    calendar_items = CalendarEntry.load_all_by_date(date)
    return {'calendar_entries': CalendarEntry.list_to_dict(calendar_items)}

def delete_entry(user, id, db: Database = None):
    if db is None:
        db = Database()
    calendar_entry = Item.load_from_db(CalendarEntry, id)
    return calendar_entry.api_delete(db)

def add_edit_entry(user, entry_id, name, date, start, end, note, address, db: Database = None):
    if db is None:
        db = Database()
    try:
        calendar_entry = Item.load_from_db(CalendarEntry, entry_id)
        calendar_entry.name = name
        calendar_entry.date = date
        calendar_entry.start = start
        calendar_entry.end = end
        calendar_entry.note = note
        calendar_entry.address = address
    except:
        calendar_entry = CalendarEntry(name, date, start, end, note, address)

    return calendar_entry.api_save(db)