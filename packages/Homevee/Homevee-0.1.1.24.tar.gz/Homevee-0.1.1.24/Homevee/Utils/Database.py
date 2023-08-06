#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3
import traceback

from Homevee.DBMigration import DBMigration
from Homevee.Helper import Logger
from Homevee.Utils import Constants


# use encrypted databases
# http://charlesleifer.com/blog/encrypted-sqlite-databases-with-python-and-sqlcipher/

class Database():
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def get_database_con():
        db_path = os.path.join(Constants.DATA_DIR, "data.db")

        # init db if not yet existing
        if not os.path.isfile(db_path):
            open(db_path, "w+")
            Database.upgrade()
        con = sqlite3.connect(db_path)
        con.text_factory = str
        con.row_factory = Database.dict_factory

        return con

    @staticmethod
    def get_server_data(key, db=None):
        item = Database.select_one("SELECT VALUE FROM SERVER_DATA WHERE KEY = :key",
                    {'key': key}, db)

        try:
            return item['VALUE']
        except Exception as e:
            return None

    @staticmethod
    def set_server_data(key, value, db=None):
        try:
            Database.insert("INSERT OR IGNORE INTO SERVER_DATA (VALUE, KEY) VALUES(:value, :key)",
                    {'value': value, 'key': key}, db)
        except:
            Database.update("UPDATE OR IGNORE SERVER_DATA SET VALUE = :value WHERE KEY = :key",
                    {'value': value, 'key': key}, db)
            
    @staticmethod
    def do_query(query, params, db_con=None):
        #Logger.log(("DATABASE_QUERY", query, params))

        if db_con is None:
            db_con = Database.get_database_con()
        with db_con:
            cur = db_con.cursor()
            cur.execute(query, params)
            return cur

    @staticmethod
    def execute_script(script, db_con=None):
        #Logger.log(("DATABASE_QUERY", query, params))

        if db_con is None:
            db_con = Database.get_database_con()
        with db_con:
            cur = db_con.cursor()
            cur.executescript(script)
        
    @staticmethod
    def select_one(query, params, db_con=None):
        try:
            cur = Database.do_query(query, params, db_con)
            output = cur.fetchone()
            cur.close()
            return output
        except:
            return None
        
    @staticmethod
    def select_all(query, params, db_con=None):
        try:
            cur = Database.do_query(query, params, db_con)
            output = cur.fetchall()
            cur.close()
            return output
        except:
            return []
        
    @staticmethod
    def insert(query, params, db_con=None):
        try:
            cur = Database.do_query(query, params, db_con)
            last_id = cur.lastrowid
            cur.close()
            return last_id
        except:
            if Logger.IS_DEBUG:
                traceback.print_exc()
        return False
        
    @staticmethod
    def update(query, params, db_con=None):
        try:
            cur = Database.do_query(query, params, db_con)
            cur.close()
            return True
        except:
            if Logger.IS_DEBUG:
                traceback.print_exc()
        return False
        
    @staticmethod
    def delete(query, params, db_con=None):
        try:
            cur = Database.do_query(query, params, db_con)
            cur.close()
            return True
        except:
            if Logger.IS_DEBUG:
                traceback.print_exc()
        return False
        
    @staticmethod
    def upgrade():
        Logger.log("Upgrading Database...")

        db = Database.get_database_con()

        with db:
            cur = db.cursor()

            migration = DBMigration()

            try:
                db_version = int(Database.get_server_data("DB_VERSION", db))
            except:
                db_version = 0

            db_script_map = migration.get_filecontent_version_map()

            db_script_versions = db_script_map.keys()

            last_version = 0

            for version in db_script_versions:
                if (version <= db_version):
                    continue

                try:
                    Logger.log("Executing DB-Upgrade-Script V"+str(version)+"...")
                    cur.executescript(db_script_map[version])
                except:
                    Database.set_server_data("DB_VERSION", version, db)

            cur.close()