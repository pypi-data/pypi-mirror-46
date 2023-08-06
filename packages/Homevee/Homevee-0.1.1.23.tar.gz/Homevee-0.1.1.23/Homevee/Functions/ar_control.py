#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import io
import json
import os
import time
import traceback
from _thread import start_new_thread

from PIL import Image

from Homevee.DeviceAPI.get_modes import get_modes
from Homevee.DeviceAPI.heating import get_thermostat_info
from Homevee.DeviceAPI.rgb_control import get_rgb_device
from Homevee.DeviceAPI.set_modes import set_modes
from Homevee.Functions.condition_actions.actions import run_scene
from Homevee.Functions.tensorflow_functions import ar_control_predict, ar_control_retrain
from Homevee.Helper import Logger
from Homevee.Item.Status import *
from Homevee.Utils import Constants
from Homevee.Utils.Constants import DATA_DIR
from Homevee.Utils.Database import Database
from Homevee.Utils.DeviceTypes import *
from Homevee.Utils.FileUtils import create_image

IS_TRAINING_TAG = "AR_CONTROL_TRAINING_RUNNING"

def upload_images(user, data, img_class, db):
    images = json.loads(data)

    counter = 0

    if (img_class == "-1" or img_class == -1):
        img_class = None

    for image in images:
        filename = "device-" + str(int(time.time())) + "_" + str(counter)

        counter += 1

        image_path = create_image(filename, "ar_control", image, optimize=True)


        cur = db.cursor()

        Database.insert("INSERT INTO AR_CONTROL_LEARNING_DATA (PATH, CONTROL_KEY) VALUES (:path, :class)",
                    {'path': image_path, 'class': img_class}, db)
        #print image

    return Status(type=STATUS_OK).get_dict()

def save_ar_control_class(user, id, data, classname, db):
    if not user.has_permission('admin'):
        return {'result': 'noadmin'}

    params = {'name': classname, 'data': data}

    if id is not None and id is not "" and id != "-1":
        params['id'] = id
        Database.update("UPDATE AR_CONTROL_CLASSES SET NAME = :name, CONTROL_DATA = :data WHERE ID = :id",
                    params, db)
    else:
        Database.insert("INSERT INTO AR_CONTROL_CLASSES (NAME, CONTROL_DATA) VALUES (:name, :data)",
                    params, db)

    return Status(type=STATUS_OK).get_dict()

def ar_control(user, image_data, db):
    filename = "device-"+str(int(time.time()))

    image_path = create_image(filename, "ar_control", image_data, optimize=True)

    Database.insert("INSERT INTO AR_CONTROL_LEARNING_DATA (PATH) VALUES (:path)",
               {'path': image_path})

    if not has_ar_control_classes(db):
        return "Noch nicht trainiert."

    predictions = ar_control_predict.predict(os.path.join(Constants.DATA_DIR, image_path))

    class_data = get_ar_class_data(predictions[0]['prediction'], db)

    Logger.log(image_path)
    Logger.log(class_data['NAME'] + ": " + str(predictions[0]['confidence']*100))
    #Logger.log(class_data)

    data = run_ar_command(user, class_data['CONTROL_DATA'], db)

    return data

def has_ar_control_classes(db):

        cur = db.cursor()
        Database.select_all("SELECT COUNT(*) FROM AR_CONTROL_CLASSES")
        result = cur.fetchone()
        count = result['COUNT(*)']

        return count > 0

def run_ar_command(user, data, db):
    data = json.loads(data)

    if data['type'] == "scene":
        run_scene(user, data['id'], db)
    elif data['type'] in [FUNKSTECKDOSE, URL_TOGGLE, URL_SWITCH, ZWAVE_SWITCH]:
        mode = get_modes(user, None, data['type'], data['id'], db)

        if mode is 0:
            mode = 1
        else:
            mode = 0

        set_modes(user, data['type'], data['id'], str(mode), db)

        return {'action': None}
    elif data['type'] in [MAX_THERMOSTAT, ZWAVE_THERMOSTAT]:
        thermostat_data = get_thermostat_info(user, None, data['type'], data['id'], db)
        return {'action': 'heating', 'data': thermostat_data, 'type': data['type'], 'id': data['id']}
    elif data['type'] in [PHILIPS_HUE_LIGHT, URL_RGB_LIGHT]:
        rgb_data = get_rgb_device(user, data['type'], data['id'], db)
        return {'action': 'rgb', 'data': rgb_data, 'type': data['type'], 'id': data['id']}
    else:
        return {'error': 'nosuchaction'}

def get_ar_class_data(id, db):

        cur = db.cursor()

        Database.select_all("SELECT * FROM AR_CONTROL_CLASSES WHERE ID = :id;", {'id': id})

        return cur.fetchone()

def start_ar_training(user, db):
    if not user.has_permission('admin'):
        return {'result': 'noadmin'}

    is_training = Database.get_server_data(IS_TRAINING_TAG, db)

    if (is_training is not None and is_training == "true"):
        return {'result': 'alreadytraining'}

    start_new_thread(training_thread, (user, None))

    return Status(type=STATUS_OK).get_dict()


def training_thread(user, d):
    db = Database.get_database_con()

    Database.set_server_data(IS_TRAINING_TAG, "true", db)

    try:
        ar_control_retrain.ar_training(user)
    except:
        if(Logger.IS_DEBUG):
                traceback.print_exc()

    Database.set_server_data(IS_TRAINING_TAG, "false", db)

def get_ar_control_classes(db):

        cur = db.cursor()

        Database.select_all("SELECT * FROM 'AR_CONTROL_CLASSES'")

        classes = []

        for row in cur.fetchall():
            item = {'id': int(row['ID']), 'name': row['NAME'], 'data': row['CONTROL_DATA']}
            classes.append(item)

        item = {'id': None, 'name': 'Nicht zugeordnet'}
        classes.append(item)

        return {'classes': classes}

def get_ar_control_class_images(image_class, show, offset, db):
    param_array = {'limit': show, 'offset': offset}

    if image_class is None or image_class == "-1" or image_class == -1:
        results = Database.select_all("SELECT * FROM 'AR_CONTROL_LEARNING_DATA' WHERE CONTROL_KEY IS NULL OR CONTROL_KEY = -1 LIMIT :limit OFFSET :offset",
                    param_array, db)
    else:
        param_array['key'] = image_class
        results = Database.select_all("SELECT * FROM 'AR_CONTROL_LEARNING_DATA' WHERE CONTROL_KEY = :key LIMIT :limit OFFSET :offset",
                    param_array, db)

    images = []

    for img in results:
        images.append(img['ID'])

    return {'images': images}

def change_ar_image_class(ids, newclass, db):
    if newclass == "-1":
        newclass = None

    ids = json.loads(ids)

    Logger.log(ids)

    for id in ids:
        Database.update("UPDATE 'AR_CONTROL_LEARNING_DATA' SET CONTROL_KEY = :key WHERE ID == :id;",
                    {'key': newclass, 'id': id}, db)

    return Status(type=STATUS_OK).get_dict()

def delete_ar_control_images(ids, db):
    #todo

    ids = json.loads(ids)

    for id in ids:
        Logger.log("deleting: "+str(id))
        item = Database.select_one("SELECT * FROM AR_CONTROL_LEARNING_DATA WHERE ID == :id;",
                    {'id': id}, db)
        if(item is not None):
            rel_path = item['PATH']

            image_path = os.path.join(DATA_DIR, rel_path)
            if os.path.exists(image_path):
                os.remove(image_path)
            else:
                Logger.log(image_path+" not found")

    for id in ids:
        Database.delete("DELETE FROM AR_CONTROL_LEARNING_DATA WHERE ID == :id;",
                    {'id': id}, db)

    return Status(type=STATUS_OK).get_dict()

def get_ar_control_image(id, db):
    item = Database.select_all("SELECT PATH FROM 'AR_CONTROL_LEARNING_DATA' WHERE ID == :id",
                {'id': id}, db)

    rel_path = item['PATH']

    path = os.path.join(DATA_DIR, rel_path)
    Logger.log(("Path: "+path))

    im = Image.open(path)

    size = 50

    image_dimensions = size, size

    im.thumbnail(image_dimensions, Image.ANTIALIAS)

    buffer = io.BytesIO()
    im.save(buffer, format="JPEG")
    encoded_string = base64.b64encode(buffer.getvalue())
    encoded_string = encoded_string.decode('utf-8')
    im.close()

    #with open(path, "rb") as image_file:
    #    encoded_string = base64.b64decode(image_file.read())

    return {'imagedata': encoded_string}

def get_performance_settings(user, db):
    if not user.has_permission('admin'):
        return Status(type=STATUS_NO_ADMIN).get_dict()

    prefix = "AR_"

    tf_data = {}

    indices = ['TF_TRAINING_STEPS', 'TF_MODEL_SIZE', 'TF_MODEL_IMAGE_SIZE']

    for index in indices:
        result = Database.get_server_data(prefix+index, db)

        if(result is not None and 'VALUE' in result):
            tf_data[index] = result['VALUE']

    return {'data': tf_data, 'graph_sizes': ar_control_retrain.get_graph_sizes(),
            'image_sizes' : ar_control_retrain.get_image_sizes()}

def set_performance_settings(user, data, db):
    if not user.has_permission('admin'):
        return {'result': 'noadmin'}

    prefix = "AR_"

    data = json.loads(data)

    indices = ['TF_TRAINING_STEPS', 'TF_MODEL_SIZE', 'TF_MODEL_IMAGE_SIZE']

    for index in indices:
        param_array = {'value': data[index], 'key': prefix+index}

        Database.update("UPDATE OR IGNORE SERVER_DATA SET VALUE = :value WHERE KEY = :key;", param_array, db)

        Database.insert("INSERT OR IGNORE INTO SERVER_DATA (VALUE, KEY) VALUES (:value, :key);", param_array, db)

    return {'result':'ok'}