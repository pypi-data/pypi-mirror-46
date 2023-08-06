import json
import os
import urllib
from _thread import start_new_thread

import pip
from packaging import version

from Homevee.Item.Status import *
from Homevee.Utils import Constants, NotificationManager
from Homevee.Utils.Database import Database


def get_homevee_update_version():
    installed_version = Constants.HOMEVEE_VERSION_NUMBER

    newest_version = get_newest_version()

    if(newest_version is None):
        return False

    if(version.parse(newest_version) > version.parse(installed_version)):
        return newest_version
    else:
        return None

def get_newest_version():
    url = "https://pypi.org/pypi/Homevee/json"

    try:
        response = urllib.request.urlopen(url).read()
        response = response.decode('utf-8')
        response_json = json.loads(response)
        version = response_json['info']['version']

        return version
    except:
        return None

def check_for_updates():
    new_version = get_homevee_update_version()

    return {
        'updates':{
            'current_version': Constants.HOMEVEE_VERSION_NUMBER,
            'new_version': new_version,
            'update_available': (new_version is not None),
            'changelog': "Changelog blabla..." #TODO add changelog or link to actual changelog
        }
    }

'''
Updates the Homevee PIP-Package
Returns true if update was successful,
returns false if there was an error
'''
def do_homevee_update(user, db):
    if(not user.has_permission("admin")):
        return {'error': "nopermission"}

    start_new_thread(update_thread, ())

    return Status(type=STATUS_OK).get_dict()

def update_thread():
    new_version = get_homevee_update_version()

    try:
        pip.main(["install", "--upgrade", "Homevee"])
    except:
        return False

    #Datenbank upgraden
    Database().upgrade()

    # TODO texte lokalisieren
    title = "Update"
    body = "Update auf Version " + new_version

    # Send notification to admin
    NotificationManager().send_notification_to_admin(title, body, Database.get_database_con())

    # Reboot the system after the update
    os.system('reboot')