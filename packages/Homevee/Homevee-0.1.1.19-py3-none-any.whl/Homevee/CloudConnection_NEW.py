#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import socket
import ssl
import time
import traceback
from _thread import start_new_thread
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from Homevee.API import API
from Homevee.Helper import Logger, translations
from Homevee.Utils.Constants import END_OF_MESSAGE
from Homevee.Utils.Database import Database
from .Helper.helper_functions import remote_control_enabled

CLOUD_URL = "test-cloud.homevee.de"
#CLOUD_URL = "premium.cloud.homevee.de"
CLOUD_PORT = 7778

#Verbindung zu Cloud herstellen

#Auf Befehl warten, ausführen und Ergebnis zurück an Server senden

class CloudConnection():
    def __init__(self):
        self.cloud_url = CLOUD_URL
        self.cloud_port = CLOUD_PORT

    def start_connection_loop(self):
        start_new_thread(self.connection_loop, ())

    def connection_loop(self):
        db = Database.get_database_con()
        REMOTE_ID, ACCESS_TOKEN = self.get_remote_data(db)
        if REMOTE_ID is None or ACCESS_TOKEN is None:
            REMOTE_ID, ACCESS_TOKEN = self.register_to_cloud(db)
            # Logger.log("NO CLOUD CONNECTION CREDENTIALS")

        print(translations.translate('your_remote_id_is') + REMOTE_ID)

        while (True):
            self.do_connection()

    def do_connection(self):
        db = Database.get_database_con()
        conn = None

        if (not remote_control_enabled(db)):
            # Logger.log("REMOTE CONTROL NOT ENABLED")
            # time.sleep(5 * 60)  # 5 Minuten warten
            time.sleep(10)
            return

        cloud_to_use = self.get_cloud_to_use(db)

        cloud_to_use = None

        if cloud_to_use is not None:
            #Logger.log("using cloud: " + cloud_to_use)
            pass
        else:
            cloud_to_use = CLOUD_URL
            #Logger.log("using default cloud: " + cloud_to_use)
            pass

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # conn.settimeout(5*60)
            # conn.connect((CLOUD_URL, CLOUD_PORT))
            # Logger.log("Connected")

            '''
            conn = ssl.wrap_socket(conn,
                                         ca_certs=SSL_FULLCHAIN,
                                         cert_reqs=ssl.CERT_REQUIRED,
                                         ssl_version=ssl.PROTOCOL_SSLv23)
            '''

            # SSL aktivieren
            conn = ssl.wrap_socket(conn)

            # Logger.log("Wrapping SSL")
            # Logger.log(("Connecting to cloud ("+CLOUD_URL+")..."))
            conn.connect((cloud_to_use, CLOUD_PORT))
            start_new_thread(self.keep_connection_alive, (conn, 60))
            # print ("SSL connected")
            # Logger.log("Connection successful!")

            REMOTE_ID, ACCESS_TOKEN = self.get_remote_data(db)
            data_dict = {'access_token': ACCESS_TOKEN, 'remote_id': REMOTE_ID}
            data = json.dumps(data_dict) + END_OF_MESSAGE

            len_send = conn.send(bytes(data, 'utf-8'))

            while 1:
                try:
                    data = conn.recv(8192).decode('utf-8')
                except:
                    data = None

                if data is None or data == "":
                    db.close()
                    conn.close()
                    return

                Logger.log("")
                Logger.log(("Received from Cloud: " + data))

                data_parts = data.split(END_OF_MESSAGE)

                for data_part in data_parts:
                    if data_part is None or data_part == "":
                        continue

                    Logger.log("")
                    Logger.log(data_part)

                    data_dict = json.loads(data_part)

                    if 'result' in data_dict:
                        Logger.log(data_dict)

                        if (data_dict['result'] == "error"):
                            Logger.log("couldn't connect to cloud")
                            time.sleep(60)  # 1 Minute warten
                    else:
                        #Logger.log("Processing data:")
                        #Logger.log(data_dict)
                        try:
                            client_id = data_dict['client_id']

                            data_dict = json.loads(data_dict['msg'])

                            msg = API().process_data(data_dict, db)

                            # start_time = time.time()
                            # compressed_message = compression.compress_string(msg)
                            # end_time = time.time()

                            # print "uncompressed: " + str(len(msg))
                            # print "compressed: " + str(len(compressed_message)) + ", time: " + str(end_time - start_time)
                            # compressed_message = compressed_message.decode('iso-8859-1').encode('utf8')

                            data = {}
                            data['msg'] = msg
                            data['client_id'] = client_id
                            data = json.dumps(data)

                            if data is None:
                                data = {'status': 'error'}
                                data['client_id'] = client_id
                                data = json.dumps(data)
                            # else:
                            #    data['client_id'] = client_id
                            #    data['msg'] = json.dumps(msg)
                            #    data = json.dumps(data)

                            data_to_send = data + END_OF_MESSAGE

                            len_send = conn.send(data_to_send.encode('utf-8'))

                            Logger.log(("Sent to remote Server (" + data_dict['action'] + ")(client: " + str(
                                client_id) + "): " + data))
                        except Exception as e:
                            #if(Logger.IS_DEBUG):
                            #    traceback.print_exc()
                            if 'status' in data_dict:
                                if data_dict['status'] == 'connectionok':
                                    #Logger.log('connectionok')
                                    pass
                                if data_dict['status'] == 'nocredentials':
                                    # Credentials wrong
                                    # deleting them from db
                                    with db:
                                        # Logger.log("wrongcredentials")
                                        time.sleep(60)  # 1 Minute warten
                                        # cur = db.cursor()
                                        # Database.delete("DELETE FROM SERVER_DATA WHERE KEY IN ('REMOTE_ID', 'REMOTE_ACCESS_TOKEN')")

        except:
            # do not print errors
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            time.sleep(5)

            if conn is not None:
                conn.close()

        db.close()

    def keep_connection_alive(self, conn, time):
        while True:
            try:
                # Send some data every minute
                time.sleep(time)
                Logger.log("sending ping")
                conn.send(1)
            except:
                break

    # Returns a tuple: (REMOTE_ID, REMOTE_ACCESS_TOKEN)
    def get_remote_data(self, db):
        # Database.delete("DELETE FROM SERVER_DATA WHERE KEY IN ('REMOTE_ACCESS_TOKEN', 'REMOTE_ID')", {}, db)

        remote_id = Database.get_server_data("REMOTE_ID", db)
        remote_access_token = Database.get_server_data("REMOTE_ACCESS_TOKEN", db)

        return (remote_id, remote_access_token)

    def get_cloud_to_use(self, db):
        try:
            REMOTE_ID, ACCESS_TOKEN = self.get_remote_data(db)

            url = 'https://cloud.homevee.de/server-api.php'  # Set destination URL here
            post_fields = {'action': 'getcloudtouse',
                           'remoteid': REMOTE_ID,
                           'accesstoken': ACCESS_TOKEN}  # Set POST fields here

            # Logger.log(url+"?action=getcloudtouse&remoteid="+REMOTE_ID+"&accesstoken="+ACCESS_TOKEN)

            request = Request(url, urlencode(post_fields).encode())
            response = urlopen(request).read().decode()

            data = json.loads(response)
            return data['cloud']
        except:
            return None

    def register_to_cloud(self, db):
        url = 'https://cloud.homevee.de/server-api.php'  # Set destination URL here
        post_fields = {'action': 'generateremoteid'}  # Set POST fields here

        request = Request(url, urlencode(post_fields).encode())
        response = urlopen(request).read().decode()

        data = json.loads(response)

        remote_id = data['remote_id']
        access_token = data['access_token']

        # Logger.log("Deine Remote-ID lautet: "+remote_id)

        # save remote id
        Database.set_server_data("REMOTE_ID", remote_id, db)
        Database.set_server_data("REMOTE_ACCESS_TOKEN", access_token, db)

        return remote_id, access_token