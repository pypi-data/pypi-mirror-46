#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item.Device import Device
from Homevee.Item.Person import Person


def add_edit_person(user, id, name, nickname, address, latitude, longitude, phonenumber, birthdate, db):
    try:
        person = Device.load_from_db(Person, id, db)
        person.name = name
        person.nickname = nickname
        person.phone_number = phonenumber
        person.address = address
        person.birthdate = birthdate
        person.longitude = longitude
        person.latitude = latitude
    except:
        person = Person(name, nickname, phonenumber, address, birthdate, longitude, latitude)

    return person.api_save()

def get_persons(db):
    persons = Person.load_all(db)
    return {'persons': Person.list_to_dict(persons)}

def delete_person(user, id, db):
    person = Device.load_from_db(Person, id)
    return person.api_delete()