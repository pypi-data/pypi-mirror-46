#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Homevee.Helper.translations import german
from Homevee.Utils import Constants

LANGUAGE = "en"
#LANGUAGE = "de"

def translate(key, language=None):
    translations = {
        'en': get_translations(),
        'de': german.get_translations()
    }

    if language is None or language not in translations:
        language = LANGUAGE

    return translations[language][key]

def translate_print(key, language=None):
    text = translate(key, language)
    print(text)

def get_translations():
    translations = {
        'no_users_create_admin': "You have not created any users yet.\nYou can create an administrator-account now.",
        'enter_password': 'Please enter a password: ',
        'password_dont_match': 'The given passwords dont match',
        'enter_username': 'Please enter a username: ',
        'your_remote_id_is': 'Your remote-id is: ',
        'homevee_server_started': "Homevee-Server (Version: " + Constants.HOMEVEE_VERSION_NUMBER + ") has been started...",
        'update_available': "There's an update for Homevee available ({})",
        'no_cloud_connection': "Could not connect to Homevee-cloud..."
    }
    return translations