import os
import subprocess
from pathlib import Path
from flask import Blueprint, request, jsonify
from ..helpers import load_json, save_json_key, update_vars

CONFIG_PATH = Path(__file__).parent/'config.json'

web_browser = Blueprint('web_browser', __name__,
                        url_prefix='/web-browser')


@web_browser.route('/state')
def get_state():
    ''' Get Web Browser state '''
    return jsonify(load_json(CONFIG_PATH)['state'])


@web_browser.route('/state', methods=['POST'])
def switch_state():
    ''' Switch Web Browser state '''
    state = request.get_json()

    if state not in ('on', 'off'):
        return jsonify('Incorrect data'), 400

    save_json_key(CONFIG_PATH, 'state', state)
    match state:
        case 'on':
            args = ['systemctl', '--user', 'start', 'chromium.service']
            subprocess.run(args, check=False)
            return jsonify('Web Browser is running')
        case 'off':
            args = ['systemctl', '--user', 'stop', 'chromium.service']
            subprocess.run(args, check=False)
            return jsonify('Web Browser is terminated')

    return jsonify('Incorrect data'), 400


@web_browser.route('/url')
def get_url():
    ''' Get Web Browser startup URL '''
    return jsonify(load_json(CONFIG_PATH)['url'])


@web_browser.route('/url', methods=['POST'])
def change_url():
    ''' Change start URL '''
    url = request.get_json()

    if not isinstance(url, str):
        return jsonify('Incorrect data'), 400

    save_json_key(CONFIG_PATH, 'url', url)
    update_vars(os.getenv('NODEBROWSER'), {'web_page=': f'"{url}"'})
    return jsonify('URL updated')
