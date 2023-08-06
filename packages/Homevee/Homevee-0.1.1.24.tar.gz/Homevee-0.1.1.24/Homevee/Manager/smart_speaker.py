from Homevee.Item.Room import Room
from Homevee.Utils.Database import Database

def get_smart_speakers(user, db):
    speakers =[]

    results = Database.select_all("SELECT * FROM SMART_SPEAKER ORDER BY LOCATION ASC", {}, db)

    for speaker in results:
        if user.has_permission(speaker['LOCATION']):
            item = {'name': speaker['NAME'], 'id': speaker['ID'], 'key': speaker['KEY'],
                    'location': speaker['LOCATION'], 'location_name': Room.get_name_by_id(speaker['LOCATION'],
                                                                                          db)}

            speakers.append(item)

    return {'speakers': speakers}

def add_edit_smart_speaker(username, db):
    return