import os
from pathlib import Path
from flask import Blueprint, request, jsonify
from .handlers import (get_files, save_files, delete_files,
                       get_dir_size, make_playlist, get_playlist_items)
from ..helpers import load_json, save_json_key

CONFIG_PATH = Path(__file__).parent/'config.json'
CONFIG = load_json(CONFIG_PATH)
MEDIA_DIR = Path(__file__).parent/'files'
PLAYLISTS_DIR = Path(MEDIA_DIR)/'playlists'
os.environ['MEDIA_PLAYLIST'] = str(PLAYLISTS_DIR/CONFIG['playlist'])

media_files = Blueprint('media_files', __name__,
                        url_prefix='/media-files')


def update_playlist():
    ''' Update playlist '''
    files = get_files(MEDIA_DIR, CONFIG['mediaExtensions'])
    make_playlist(files, os.getenv('MEDIA_PLAYLIST'))


@media_files.route('/')
def media():
    ''' Return list of media files '''
    files = get_files(MEDIA_DIR, CONFIG['mediaExtensions'])
    return jsonify(files)


@media_files.route('/add', methods=['POST'])
def upload_media():
    ''' Upload files '''
    if 'media' not in request.files:
        return jsonify('No media'), 400

    files = []
    for file in request.files.getlist('media'):
        if Path(file.filename).suffix in CONFIG['mediaExtensions']:
            files.append(file)

    if files:
        save_files(files, MEDIA_DIR)
        update_playlist()
        return jsonify('Upload is done'), 201
    return jsonify('Incorrect file extension'), 400


@media_files.route('/delete', methods=['DELETE'])
def delete_media():
    ''' Delete media files '''
    try:
        files = request.get_json()
        if not isinstance(files, list):
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    delete_files(files, MEDIA_DIR)
    update_playlist()
    return jsonify('Files removed')


@media_files.route('/size')
def media_size():
    ''' Return size of "files" directory '''
    return jsonify(get_dir_size(MEDIA_DIR, 2))


@media_files.route('/playlists')
def get_playlists():
    ''' Returns avalible playlists '''
    playlists = get_files(PLAYLISTS_DIR, '.m3u', False)
    playlists = [int(p) for p in playlists]
    playlists.sort()
    return jsonify(playlists)


@media_files.route('/playlists/add', methods=['POST'])
def add_new_playlist():
    ''' Create playlist '''
    try:
        content = request.get_json()
        if not isinstance(content, list):
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    playlists = get_files(PLAYLISTS_DIR, suffix=False)
    playlists = [int(i) for i in playlists]
    playlists.sort()

    if len(playlists) >= CONFIG['maxPlaylist']:
        return jsonify(f"Exceed max number of playlists - {CONFIG['maxPlaylist']}"), 400

    new_id = None
    test_range = range(1, CONFIG['maxPlaylist'] + 1)
    for item in test_range:
        if not item in playlists:
            new_id = item
            break

    if make_playlist(content, PLAYLISTS_DIR/f'{new_id}.m3u'):
        return jsonify(f'Playlist #{new_id} created')
    return jsonify('Failed to create playlist'), 204


@media_files.route('/playlists/delete', methods=['DELETE'])
def remove_playlists():
    ''' Remove playlist '''
    try:
        data = request.get_json()
        all_int = all(isinstance(item, int) for item in data)
        if not isinstance(data, list) or not all_int:
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    playlists = get_files(PLAYLISTS_DIR, suffix=False)
    playlists = [int(p) for p in playlists]

    for item in data:
        if item in playlists:
            delete_files([f'{item}.m3u'], PLAYLISTS_DIR)

    return jsonify('Playlist(s) removed')


@media_files.route('/playlists/content/<int:playlist_id>')
def get_playlist_content(playlist_id):
    ''' Return playlist content '''
    content = get_playlist_items(PLAYLISTS_DIR/f'{playlist_id}.m3u')
    if content is None:
        return jsonify('Playlist Not Found'), 404
    return jsonify(content)


@media_files.route('/playlists/content/<int:playlist_id>', methods=['PUT'])
def update_playlist_content(playlist_id):
    ''' Update playlist content '''
    try:
        data = request.get_json()
        all_str = all(isinstance(item, str) for item in data)
        if not isinstance(data, list) or not all_str:
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    playlists = get_files(PLAYLISTS_DIR, suffix=False)
    playlists = [int(p) for p in playlists]

    if playlist_id not in playlists:
        return jsonify('Playlist Not Found'), 404

    make_playlist(data, PLAYLISTS_DIR/f'{playlist_id}.m3u')
    return jsonify(f'Playlist #{playlist_id} updated')


@media_files.route('/playlists/default')
def get_default_playlist():
    ''' Get default playlist '''
    playlist_id = Path(os.getenv('MEDIA_PLAYLIST')).stem
    return jsonify(int(playlist_id))


@media_files.route('/playlists/default', methods=['POST'])
def set_playlist():
    ''' Set default playlist '''
    try:
        new_id = request.get_json()
        if not isinstance(new_id, int):
            raise TypeError
    except TypeError:
        return jsonify('Incorrect data'), 400

    playlists = get_files(PLAYLISTS_DIR, '.m3u', False)
    for item in playlists:
        if int(item) == new_id:
            save_json_key(CONFIG_PATH, 'playlist', f'{new_id}.m3u')
            os.environ['MEDIA_PLAYLIST'] = str(
                PLAYLISTS_DIR/f'{new_id}.m3u')
            return jsonify(f'Playlist #{new_id} is default')

    return jsonify(f'Playlist #{new_id} Not Found'), 400
