#!flask/bin/python
from flask import Blueprint, request

from Homevee.API import API
from Homevee.Utils.Database_NEW import Database

ProcessDataAPI = Blueprint('ProcessDataAPI', __name__, template_folder='templates')

@ProcessDataAPI.route('/processdata/<data>', methods=['GET'])
def is_premium(data):
    print("processdata")

    assert data == request.view_args['data']

    msg = API().process_data(data, Database())
    return msg