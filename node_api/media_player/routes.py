import os
from pathlib import Path
import subprocess
from flask import Blueprint, request, jsonify
from .handlers import vlc_rc, update_settings
from ..helpers import load_json, save_json, save_json_key, update_vars

CONFIG_PATH = Path(__file__).parent/'config.json'
CONFIG = load_json(CONFIG_PATH)
PLAYLIST = os.getenv('MEDIA_PLAYLIST')
media_player = Blueprint('media_player', __name__,
                         url_prefix='/media-player')


@media_player.route('/state')
def get_state():
    ''' Get Media Player state '''
    return jsonify(load_json(CONFIG_PATH)['state'])


@media_player.route('/state', methods=['POST'])
def switch_state():
    ''' Switch Media Player state '''
    try:
        state = request.get_json()
        if not isinstance(state, str) or state not in ('on', 'off'):
            raise ValueError
        save_json_key(CONFIG_PATH, 'state', state)
    except ValueError:
        return jsonify('Incorrect data'), 400

    match state:
        case 'on':
            config = load_json(CONFIG_PATH)
            playlist = os.getenv('MEDIA_PLAYLIST')
            player_script = os.getenv('NODEPLAYER')
            args = ['systemctl', '--user', 'start', 'vlc.service']
            var_dict = {
                'media=': f'"{playlist}"',
                'module=': f'"{config["module"]}"',
                'playback=': f'"{" ".join(config["playback"])}"'
            }

            update_vars(player_script, var_dict)
            subprocess.run(args, check=False)
            return jsonify('Player is on')
        case 'off':
            args = ['systemctl', '--user', 'stop', 'vlc.service']
            subprocess.run(args, check=False)
            return jsonify('Player is off')

    return jsonify('Incorrect data'), 400


@media_player.route('/control', methods=['POST'])
def control_player():
    ''' Execute player commands '''
    data = request.get_json()

    try:
        command = data['command']
    except KeyError:
        return jsonify('Incorrect data'), 400

    try:
        value = data['value']
    except KeyError:
        value = ''

    match vlc_rc(command, value):
        case True:
            return jsonify(f'{command} executed')
        case False:
            return jsonify('Incorrect data'), 400
        case None:
            return jsonify('Media player not available'), 503


@media_player.route('/settings')
def show_settings():
    ''' Return player settings '''
    settings = load_json(CONFIG_PATH)
    return settings


@media_player.route('/settings', methods=['POST'])
def update_settings_handler():
    ''' Update player settings '''
    data = request.get_json()
    settings = load_json(CONFIG_PATH)
    new_settings = update_settings(settings, data)
    save_json(CONFIG_PATH, new_settings)
    return jsonify('Settings applied')
