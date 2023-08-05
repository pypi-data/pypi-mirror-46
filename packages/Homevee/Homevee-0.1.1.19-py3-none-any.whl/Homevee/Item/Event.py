import traceback

from Homevee.Exception import DatabaseSaveFailedException, InvalidParametersException
from Homevee.Helper import Logger
from Homevee.Item import Item
from Homevee.Utils.Database import Database


class Event(Item):
    def __init__(self, text, type, timestamp=None, id=None):
        super(Event, self).__init__()

        self.timestamp = timestamp
        self.text = text
        self.type = type
        self.id = id

    def delete(self, db=None):
        try:
            Database.delete("DELETE FROM EVENTS WHERE ID == :id", {'id': self.id}, db)
            return True
        except:
            return False

    def save_to_db(self, db=None):
        try:
            if (self.id is None or self.id == ""):
                Database.insert("""INSERT INTO EVENTS (TEXT, TYPE) VALUES (:text, :type)""",
                            {'text': self.text, 'type': self.type}, db)
            # update
            else:
                Database.update("""UPDATE EVENTS SET TEXT = :text, TYPE = :type WHERE ID = :id""",
                            {'text': self.text, 'type': self.type, 'id': self.id}, db)
                #TODO add generated id to object
        except:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            raise DatabaseSaveFailedException("Could not save event to database")

    def build_dict(self):
        dict = {
            'id': self.id,
            'timestamp': self.timestamp,
            'text': self.text,
            'type': self.type
        }
        return dict

    @staticmethod
    def load_all_from_db(query, params, db=None):
        items = []
        for result in Database.select_all(query, params, db):
            item = Event(result['TEXT'], result['TYPE'], result['TIMESTAMP'], result['ID'])
            items.append(item)
        return items

    @staticmethod
    def load_all_from_db_desc_date_by_type(offset, limit, type=None, db=None):
        params = {'limit': limit, 'offset': offset}

        where_clause = ""

        if type is not None and type != "":
            params['type'] = type
            where_clause = "WHERE TYPE == :type "

        query = "SELECT * FROM 'EVENTS' " + where_clause + "ORDER BY TIMESTAMP DESC LIMIT :limit OFFSET :offset"

        return Event.load_all_from_db(query, params, db)

    @staticmethod
    def get_unseen_events(user, db):
        last_checked = user.events_last_checked

        events = Event.load_all_from_db("SELECT * FROM 'EVENTS' WHERE TIMESTAMP > :time",
                        {'time': last_checked}, db)

        return len(events)

    @staticmethod
    def load_all_types_from_db(types, db=None):
        query = 'SELECT * FROM EVENTS WHERE TYPE IN (%s)' % ','.join('?'*len(types)), types
        return Event.load_all_from_db(query, {}, db)

    @staticmethod
    def load_all(db=None):
        return Event.load_all_from_db('SELECT * FROM EVENTS', {}, db)

    @staticmethod
    def create_from_dict(dict):
        try:
            id = dict['id']
            timestamp = dict['timestamp']
            text = dict['text']
            type = dict['type']

            item = Event(text, type, timestamp, id)

            return item
        except:
            raise InvalidParametersException("Event.create_from_dict(): invalid dict")