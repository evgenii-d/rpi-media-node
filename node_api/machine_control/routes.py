from pathlib import Path
from flask import Blueprint, request, jsonify
from .handlers import exec_command
from ..helpers import save_json

CONFIG = Path(__file__).parent/'config.json'
machine_control = Blueprint('machine_control', __name__,
                            url_prefix='/machine-control')


@machine_control.route('/', methods=['POST'])
def command_handler():
    ''' Process command '''
    command = request.get_json()
    if not isinstance(command, str):
        return jsonify('Incorrect data'), 400

    if command == 'hostname':
        save_json(CONFIG, {'hostname': True})
        return jsonify(f'{str(command).upper()} - reboot required')

    if exec_command(command):
        return jsonify(f'{str(command).upper()} performed')

    return jsonify('Incorrect data'), 400
