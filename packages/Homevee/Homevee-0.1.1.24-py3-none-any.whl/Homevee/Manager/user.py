#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Exception import ItemNotFoundException
from Homevee.Item.Status import *
from Homevee.Item.User import User, Permission


def set_user_fcm_token(user, token, db):
    user.fcm_token = token

    try:
        user.save_to_db(db)
        return Status(type=STATUS_OK).get_dict()
    except:
        return Status(type=STATUS_ERROR).get_dict()

def has_users(db):
    #with db:
    #    # Nutzer laden
    #    cur = db.cursor()
    #    cur.execute("SELECT COUNT(*) FROM USERDATA")
    #    result = cur.fetchone()
    #    if result['COUNT(*)'] > 0:
    #        return True
    #    else:
    #        return False

    users = User.load_all(db)
    return len(users) > 0

def get_users(user, db):
    if not user.hash_password("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    users = User.load_all(db)
    return {'userdata': User.list_to_dict(users)}

def delete_user(user, user_to_delete, db):
    if not user.has_permission("admin"):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    user_to_delete = User.load_username_from_db(user_to_delete, db)
    return user_to_delete.api_delete()

def add_edit_user(user, name, psw, ip, permissions, db):
    if not user.has_permission("admin"):
        if user.username != name:
            return Status(type=STATUS_NO_PERMISSION).get_dict()

    hashed_pw, salt = User.hash_password(psw)

    try:
        edit_user = User.load_username_from_db(name, db)

        if not (psw == "" or psw is None):
            edit_user.hashed_password = hashed_pw
            edit_user.salt = salt

        edit_user.ip = ip
        edit_user.permissions = Permission.create_list_from_json(permissions)

    except ItemNotFoundException:
        edit_user = User(username=name, hashed_password=hashed_pw, salt=salt, ip=ip,
                         permissions=Permission.create_list_from_json(permissions),
                         at_home=False, fcm_token=None, current_location=None,
                         dashboard_data=None, events_last_checked=0)

    return edit_user.api_save()