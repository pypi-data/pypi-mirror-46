#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.Cronjob import IntervalCronjob
from Homevee.DeviceAPI.zwave.get_devices import set_device_value
from Homevee.DeviceAPI.zwave.utils import do_zwave_request
from Homevee.Utils.Database import Database
from Homevee.Utils.DeviceTypes import *


class ZWaveValueLoaderCronjob(IntervalCronjob):
    def __init__(self):
        super(ZWaveValueLoaderCronjob, self).__init__(task_name="ZWaveValueLoaderCronjob", interval_seconds=5*60)

    def task_to_do(self, *args):
        self.load_zwave_values()

    def load_zwave_values(self):
        db = Database.get_database_con()



        # Alle Z-Wave Gerätetypen durchlaufen und den aktuellen Wert in Datenbank schreiben

        #Stromzähler
        TYPE = ZWAVE_POWER_METER
        data = Database.select_all("SELECT * FROM ZWAVE_POWER_METER", {}, db)

        for item in data:
            ID = item['DEVICE_ID']
            result = do_zwave_request("/ZAutomation/api/v1/devices/" + ID, db)

            if result is None or result['code'] != 200:
                value = "N/A"
            else:
                value = result['data']['metrics']['level']

            set_device_value(TYPE, ID, value, db)

        #Thermostat
        TYPE = ZWAVE_THERMOSTAT
        data = Database.select_all("SELECT * FROM ZWAVE_THERMOSTATS", {}, db)

        for item in data:
            ID = item['THERMOSTAT_ID']
            result = do_zwave_request("/ZAutomation/api/v1/devices/" + ID, db)

            if result is None or result['code'] != 200:
                value = "N/A"
            else:
                value = result['data']['metrics']['level']

            set_device_value(TYPE, ID, value, db)

        #Sensor
        TYPE = ZWAVE_SENSOR
        data = Database.select_all("SELECT * FROM ZWAVE_SENSOREN", {}, db)

        for item in data:
            ID = item['ID']
            result = do_zwave_request("/ZAutomation/api/v1/devices/" + ID, db)

            if result is None or result['code'] != 200:
                value = "N/A"
            else:
                value = result['data']['metrics']['level']

                #if item['VALUE'] != value:
                    #trigger automation

            set_device_value(TYPE, ID, value, db)

        #Schalter
        TYPE = ZWAVE_SWITCH
        data = Database.select_all("SELECT * FROM ZWAVE_SWITCHES", {}, db)

        for item in data:
            ID = item['ID']
            result = do_zwave_request("/ZAutomation/api/v1/devices/" + ID, db)

            if result is None or result['code'] != 200:
                value = "N/A"
            else:
                value = result['data']['metrics']['level']

                value = value == "on"

            set_device_value(TYPE, ID, value, db)