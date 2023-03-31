import os
import json
import subprocess
import time
import uuid
import platform
import threading
from pathlib import Path
import requests
from waitress import serve
from flask_cors import CORS
from flask import Flask, render_template
from node_api.helpers import load_json, save_json
from node_api.machine_control.routes import machine_control
from node_api.media_files.routes import media_files
from node_api.media_player.routes import media_player
from node_api.node_details.routes import node_details
from node_api.web_browser.routes import web_browser
from node_api.web_server.routes import web_server

app = Flask(__name__)
CORS(app)
app.config.from_file('config.json', load=json.load)
app.register_blueprint(machine_control)
app.register_blueprint(media_files)
app.register_blueprint(media_player)
app.register_blueprint(node_details)
app.register_blueprint(web_browser)
app.register_blueprint(web_server)


@app.route('/')
def index_handler():
    ''' Index page '''
    return render_template('index.html')


@app.route('/media-control')
def media_control():
    ''' Media control page '''
    return render_template('media-control.html')


@app.route('/browser-control')
def browser_control():
    ''' Browser control page '''
    return render_template('browser-control.html')


@app.route('/server-control')
def server_control():
    ''' Server control page '''
    return render_template('server-control.html')


def apps_loader():
    ''' Start applications by API '''
    time.sleep(app.config['APPS_DELAY'])
    base_url = f"http://127.0.0.1:{app.config['PORT']}"
    apps = ['/web-server/state', '/web-browser/state', '/media-player/state']

    for api in apps:
        try:
            state = requests.get(f'{base_url}{api}', timeout=1)
            requests.post(f'{base_url}{api}', json=state.json(), timeout=1)
        except requests.exceptions.ReadTimeout:
            pass


def change_hostname(config):
    ''' Change hostname and reboot node '''
    if platform.system() != 'Linux':
        return

    save_json(config, {'hostname': False})
    new_hostname = str(uuid.uuid4())[0:13]
    subprocess.run(
        ['sudo', 'hostnamectl', 'set-hostname', new_hostname], check=False)
    subprocess.run(
        ['sudo', 'shutdown', '-r', 'now'], check=False)


def main():
    ''' Run application '''
    system_scripts = Path(__file__).parent/'system_scripts'
    os.environ['NODEBROWSER'] = str(system_scripts/'run_chromium.sh')
    os.environ['NODEPLAYER'] = str(system_scripts/'run_vlc.sh')

    mc_config = Path(__file__).parent/'node_api/machine_control/config.json'
    hostname = load_json(mc_config)['hostname']
    if hostname:
        change_hostname(mc_config)

    loader_thread = threading.Thread(target=apps_loader)
    loader_thread.daemon = True
    loader_thread.start()

    if app.config['DEBUG']:
        app.run(host='0.0.0.0')
    else:
        serve(app, host='0.0.0.0', port=app.config['PORT'])


if __name__ == '__main__':
    main()
