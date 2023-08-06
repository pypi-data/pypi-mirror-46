import json

from Homevee.Item import Item
from Homevee.Item.Room import Room


class Permission(Item):
    def __init__(self, permission_key, name=None):
        super(Permission, self).__init__()

        if name is not None:
            self.name = name
        else:
            if permission_key == "admin":
                self.name = "Administrator"
            else:
                self.name = Room.get_name_by_id(permission_key, None)

        self.key = permission_key

    def build_dict(self):
        dict = {
            'key': self.key,
            'name': self.name
        }
        return dict

    @staticmethod
    def create_list_from_json(json_string):
        data = json.loads(json_string)

        permissions = []

        for item in data['permissions']:
            permissions.append(Permission(item))

        return permissions

    @staticmethod
    def list_to_dict(list):
        permissions = []

        for item in list:
            permissions.append(item.get_dict())

        return permissions

    @staticmethod
    def list_from_dict(dict):
        permissions = []

        for item in dict:
            permissions.append(Permission(item['key'], item['name']))

        return permissions


    @staticmethod
    def get_json_list(permissions):
        data = []

        for permission in permissions:
            data.append(permission.key)

        permission_data = {'permissions': data}

        return json.dumps(permission_data)