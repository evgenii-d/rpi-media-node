import socket
from pathlib import Path
from flask import Blueprint, request, jsonify
from ..helpers import load_json, save_json

CONFIG_PATH = Path(__file__).parent/'config.json'
NAME_MAX_CHAR = load_json(CONFIG_PATH)['nameMaxChar']

node_details = Blueprint('node_details', __name__,
                         url_prefix='/node-details')


@node_details.route('/name')
def show_name():
    ''' Return node name'''
    config = load_json(CONFIG_PATH)
    return jsonify(config['name'])


@ node_details.route('/name', methods=['POST'])
def set_name():
    ''' Set node name '''
    try:
        new_name = request.get_json()
        if not isinstance(new_name, str):
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    if len(new_name) <= NAME_MAX_CHAR:
        config = load_json(CONFIG_PATH)
        config['name'] = new_name
        save_json(CONFIG_PATH, config)
        return jsonify('New name applied')

    return jsonify('Incorrect data'), 400


@ node_details.route('/hostname')
def hostname_handler():
    ''' Return hostname '''
    return jsonify(socket.gethostname())
