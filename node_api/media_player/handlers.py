import socket


def vlc_rc(command: str, value: str = '',
           host: str = '127.0.0.1', port: int = 50000) -> bool | None:
    ''' Send commands to RC interface '''
    allow_list = ('play', 'stop', 'prev', 'next',
                  'goto', 'quit', 'volume', 'stats')

    if command not in allow_list:
        return False

    command = f'{command} {value}' if value else command

    try:
        rc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rc_socket.connect((host, port))
        rc_socket.send(command.encode())
        rc_socket.close()
        return True
    except OSError:
        return None


def update_settings(settings: dict, new_settings: dict) -> dict:
    ''' Update player settings '''
    for key in new_settings.keys():
        value = new_settings[key]

        match key:
            case 'volume':
                try:
                    if 0 <= value <= 320:
                        settings['volume'] = value
                        vlc_rc('volume', value)
                except TypeError:
                    pass
            case 'module':
                if value in ('any', 'gles2'):
                    settings['module'] = value
                    print(value)
            case 'playback':
                if isinstance(value, list):
                    for option in value:
                        if option not in ('-L', '-R'):
                            value.remove(option)
                    settings['playback'] = value
    return settings
