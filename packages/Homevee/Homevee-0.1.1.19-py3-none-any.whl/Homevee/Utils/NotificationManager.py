import json
import socket
import ssl
import traceback

# https://github.com/olucurious/PyFCM
from Homevee.Helper import Logger
from Homevee.Utils.Database import Database
from .Constants import END_OF_MESSAGE


class NotificationManager():
    def __init__(self):
        return

    def send_notification(self, registration_ids, message_title, message_body, click_action=None):
        CLOUD_URL = "free.cloud.homevee.de"
        CLOUD_PORT = 7778

        conn = None

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(5 * 60)

            # SSL aktivieren
            conn = ssl.wrap_socket(conn)

            # Logger.log("Wrapping SSL")

            conn.connect((CLOUD_URL, CLOUD_PORT))

            # print ("SSL connected")

            # Logger.log("Connection successful!")

            message_data = {
                'title': message_title,
                'msg': message_body,
                'clickaction': click_action
            }

            data_dict = {'registration_ids': registration_ids, 'message_data': json.dumps(message_data)}

            data = json.dumps(data_dict) + END_OF_MESSAGE

            len_send = conn.send(data)

            while 1:
                data = conn.recv(8192)

                if data == "":
                    conn.close()
                    return

                Logger.log("")
                Logger.log(("Received: " + data))

                data_parts = data.split(END_OF_MESSAGE)
                for data_part in data_parts:
                    if data_part is None or data_part == "":
                        continue

                    Logger.log("")
                    Logger.log(data_part)

                    data_dict = json.loads(data_part)

                    if 'result' in data_dict:
                        Logger.log(data_dict)

                break

        except Exception as e:
            if(Logger.IS_DEBUG):
                    traceback.print_exc()

            if conn is not None:
                conn.close()

    def send_notification_to_users(self, users, message_title, message_body, db, click_action=None):
        registration_ids = self.get_user_tokens(users, db)

        self.send_notification(registration_ids, message_title, message_body, click_action)

    def send_notification_to_admin(self, message_title, message_body, db, click_action=None):
        admins = []

        self.send_notification_to_users(admins, message_title, message_body, db, click_action)

    def get_user_tokens(self, users, db):
            tokens = []

            with db:
                if (len(users) is 0):
                    cur = db.cursor()

                    Database.select_all("SELECT TOKEN FROM PUSH_NOTIFICATION_TOKENS")

                    for item in cur.fetchall():
                        tokens.append(item['TOKEN'])
                else:
                    cur = db.cursor()

                    for user in users:
                        Database.select_all("SELECT TOKEN FROM PUSH_NOTIFICATION_TOKENS WHERE USERNAME = :user",
                                    {'user': user})

                        for item in cur.fetchall():
                            if (item['TOKEN'] is not None):
                                tokens.append(item['TOKEN'])

            #print users
            #print tokens

            return tokens

    def delete_user_tokens(self, username, db):
            Database.delete("DELETE FROM PUSH_NOTIFICATION_TOKENS WHERE USERNAME = :user", {'user': username})