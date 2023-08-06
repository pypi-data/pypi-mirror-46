#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_all_api_key_data(user, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    services = [
        {'servicename': 'Open Weather Map',
         'description': 'Open Weather Map stellt Wetterdaten und -vorhersagen bereit.', 'registerkeyurl': '',
         'servicelogourl': 'https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/logo_OpenWeatherMap_orange.svg'},
        {'servicename': 'IMDB', 'description': 'IMDB ist eine internationale Filmdatenbank', 'registerkeyurl': '',
         'servicelogourl': 'http://ia.media-imdb.com/images/G/01/imdb/images/mobile/imdb-logo-responsive@2-868559777._CB514893749_.png'}
    ]

    output = []

    for service in services:
        service['key'] = get_api_key(service['servicename'], db)

        output.append(service)

    return {'apikeys': output}

def get_api_key(servicename, db):
    service_data = Database.select_one("SELECT API_KEY FROM API_KEYS WHERE SERVICE_NAME = :name", {'name': servicename}, db)

    try:
        key = service_data['API_KEY']
    except TypeError as e:
        #key doesn't exist
        return None

    return key

def set_api_key(user, service, api_key, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    params = {'key': api_key, 'name': service}

    Database.update("UPDATE OR IGNORE API_KEYS SET API_KEY = :key WHERE SERVICE_NAME = :name;", params, db)
    Database.insert("INSERT OR IGNORE INTO API_KEYS (API_KEY, SERVICE_NAME) VALUES (:key, :name);", params, db)

    return Status(type=STATUS_OK).get_dict()