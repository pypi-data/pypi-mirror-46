# https://github.com/olucurious/PyFCM
from Homevee.Helper.HomeveeCloud import HomeveeCloudWrapper
from Homevee.Item.User import User
from Homevee.Utils.Database import Database


class NotificationManager():
    def __init__(self):
        return

    def send_notification(self, registration_ids, message_title, message_body, click_action=None):
        cloud_wrapper = HomeveeCloudWrapper()
        message_data = {'title': message_title, 'msg': message_body, 'clickaction': click_action}
        cloud_wrapper.send_push_notification(registration_ids, message_data)

    def send_notification_to_users(self, users, message_title, message_body, db, click_action=None):
        registration_ids = self.get_user_tokens(users, db)
        self.send_notification(registration_ids, message_title, message_body, click_action)

    def send_notification_to_admin(self, message_title, message_body, db, click_action=None):
        admins = User.load_by_permission("admin", db)
        self.send_notification_to_users(admins, message_title, message_body, db, click_action)

    def get_user_tokens(self, users=None, db=None):
            tokens = []

            if users is None or (len(users) is 0):
                cur = db.cursor()

                Database.select_all("SELECT TOKEN FROM PUSH_NOTIFICATION_TOKENS", db)

                for item in cur.fetchall():
                    tokens.append(item['TOKEN'])
            else:
                cur = db.cursor()

                for user in users:
                    Database.select_all("SELECT TOKEN FROM PUSH_NOTIFICATION_TOKENS WHERE USERNAME = :user",
                                {'user': user}, db)

                    for item in cur.fetchall():
                        if (item['TOKEN'] is not None):
                            tokens.append(item['TOKEN'])

            #print users
            #print tokens

            return tokens

    def delete_user_tokens(self, username, db):
            Database.delete("DELETE FROM PUSH_NOTIFICATION_TOKENS WHERE USERNAME = :user", {'user': username}, db)