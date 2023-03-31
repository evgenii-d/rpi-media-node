import shutil
import subprocess
import zipfile
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file
from ..helpers import load_json, save_json_key

PUBLIC_DIR = Path(__file__).parent/'public'
ZIP_ARCHIVE = Path(__file__).parent/'archive.zip'
CONFIG_PATH = Path(__file__).parent/'config.json'

web_server = Blueprint('web_server', __name__, url_prefix='/web-server')


@web_server.route('/state')
def get_state():
    ''' Get Web Server state '''
    return jsonify(load_json(CONFIG_PATH)['state'])


@web_server.route('/state', methods=['POST'])
def switch_state():
    ''' Switch Web Server state '''
    state = request.get_json()

    if state not in ('on', 'off'):
        return jsonify('Incorrect data'), 400

    save_json_key(CONFIG_PATH, 'state', state)
    match state:
        case 'on':
            args = ['systemctl', '--user', 'start', 'web_server.service']
            subprocess.run(args, check=False)
            return jsonify('Web Server is running')
        case 'off':
            args = ['systemctl', '--user', 'stop', 'web_server.service']
            subprocess.run(args, check=False)
            return jsonify('Web Server is not running')

    return jsonify('Incorrect data'), 400


@web_server.route('/archive', methods=['POST'])
def upload_handler():
    ''' Upload zip archive and extract to public folder '''
    if ('archive' not in request.files or
            request.files['archive'].mimetype.find('zip') == -1):
        return jsonify('Archive not found'), 204

    with open(ZIP_ARCHIVE, 'wb') as file:
        shutil.copyfileobj(request.files['archive'], file)

    if not zipfile.is_zipfile(ZIP_ARCHIVE):
        return jsonify('Cannot open file as archive'), 400

    shutil.rmtree(PUBLIC_DIR)
    Path.mkdir(PUBLIC_DIR)
    shutil.unpack_archive(ZIP_ARCHIVE, PUBLIC_DIR)
    return jsonify('Archive uploaded')


@web_server.route('/archive')
def archive_handler():
    ''' Return zip archive '''
    try:
        return send_file(ZIP_ARCHIVE, as_attachment=True)
    except FileNotFoundError:
        return jsonify('Archive not found'), 204
