import json
import os
import urllib
from _thread import start_new_thread

import pip
from packaging import version

from Homevee.Item import User
from Homevee.Item.Status import *
from Homevee.Utils import Constants
from Homevee.Utils.Database_NEW import Database
from Homevee.Utils.NotificationManager import NotificationManager


def get_homevee_update_version():
    """
    Gets the updateable homevee-version
    :return: None if no newer version found, version number otherwise
    """
    installed_version = Constants.HOMEVEE_VERSION_NUMBER

    newest_version = get_newest_version()

    if(newest_version is None):
        return None

    if(version.parse(newest_version) > version.parse(installed_version)):
        return newest_version
    else:
        return None

def get_newest_version() -> str:
    """
    Gets the newest homevee-version from pypi
    :return: the version string or None
    """
    url = "https://pypi.org/pypi/Homevee/json"

    try:
        response = urllib.request.urlopen(url).read()
        response = response.decode('utf-8')
        response_json = json.loads(response)
        version = response_json['info']['version']

        return version
    except:
        return None

def check_for_updates() -> dict:
    """
    Checks if a new homevee-version is available on pypi
    :return:
    """
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
def do_homevee_update(user: User, db: Database) -> dict:
    """
    Starts the homevee update-process
    :param user: the user
    :param db: the database connection
    :return: the status of the update process
    """
    if(not user.has_permission("admin")):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    start_new_thread(update_thread, ())

    return Status(type=STATUS_OK).get_dict()

def update_thread():
    """
    The thread for the update process of homevee
    :return:
    """
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
    NotificationManager().send_notification_to_admin(title, body, Database())

    # Reboot the system after the update
    os.system('reboot')