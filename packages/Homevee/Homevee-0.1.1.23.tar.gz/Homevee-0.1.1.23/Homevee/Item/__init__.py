from Homevee.Exception import InvalidParametersException, AbstractFunctionCallException, ItemNotFoundException
from Homevee.Item.Status import *


class Item():
    def __init__(self):
        pass

    def api_delete(self, db=None):
        try:
            if self.delete(db):
                return Status(type=STATUS_OK).get_dict()
        except:
            pass
        return Status(type=STATUS_ERROR).get_dict()

    def api_save(self, db=None):
        try:
            self.save_to_db(db)
            return Status(type=STATUS_OK).get_dict()
        except:
            pass
        return Status(type=STATUS_ERROR).get_dict()

    def delete(self, db=None):
        raise AbstractFunctionCallException("Item.delete() is abstract")

    def save_to_db(self, db=None):
        raise AbstractFunctionCallException("Item.save_to_db() is abstract")

    def build_dict(self):
        raise AbstractFunctionCallException("Item.build_dict() is abstract")

    def get_dict(self, fields=None):
        dict = self.build_dict()

        if (fields is None):
            return dict
        else:
            try:
                output_dict = {}

                for field in fields:
                    output_dict[field] = dict[field]

                return output_dict
            except:
                raise InvalidParametersException("InvalidParams given for get_dict()")

    @staticmethod
    def load_all_ids_from_db(ids, db=None):
        raise AbstractFunctionCallException("Item.load_all_ids_from_db() is abstract")

    @staticmethod
    def load_all_from_db(query, params, db=None):
        raise AbstractFunctionCallException("Item.load_all_from_db() is abstract")

    @staticmethod
    def load_from_db(module, id, db=None):
        items = module.load_all_ids_from_db([id], db)

        if ((len(items) == 0) or (str(items[0].id) != str(id))):
            raise ItemNotFoundException("Could not find id: " + id)
        else:
            return items[0]

    @staticmethod
    def create_from_dict(dict):
        raise AbstractFunctionCallException("Item.create_from_dict() is abstract")

    @staticmethod
    def list_to_dict(list):
        data = []

        for item in list:
            data.append(item.get_dict())

        return data