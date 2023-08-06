#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Utils.Database_NEW import Database


def get_summary(user, db: Database = None):
    if db is None:
        db = Database()
    return