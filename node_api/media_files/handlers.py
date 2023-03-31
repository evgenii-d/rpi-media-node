import os
from pathlib import Path
from werkzeug.utils import secure_filename


def get_dir_size(dir_path: str | Path, units: int = 0) -> int | float:
    ''' Return folder size (bytes by default)
    units: int [optional]
        1 - KiB, 2 - MiB, 3 - GiB, 4 - TiB
    '''
    size = 0
    if Path(dir_path).is_file():
        return size

    for child in Path(dir_path).iterdir():
        size += child.stat().st_size

    if 0 < units < 5:
        size = size / 1024 ** units
    return round(size, 1)


def save_files(file_list: list, dir_path: str):
    ''' Save files to dir '''
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    for file in file_list:
        path = Path(dir_path, secure_filename(file.filename))
        file.save(path)


def get_files(dir_path: str | Path, extensions: list = None, suffix: bool = True) -> list:
    ''' Return list of files from directory '''
    files = []

    if extensions:
        for child in Path(dir_path).iterdir():
            if child.suffix in extensions and child.is_file():
                files.append(child)
    else:
        for child in Path(dir_path).iterdir():
            if child.is_file():
                files.append(child)

    for i, file in enumerate(files):
        files[i] = file.name if suffix else file.stem

    files.sort()
    return files


def delete_files(files: list, dir_path: str | Path):
    ''' Delete files from dir '''

    for item in files:
        for child in Path(dir_path).iterdir():
            if child.is_file() and child.name == item:
                os.remove(child)


def make_playlist(files: list, save_path: str | Path) -> bool:
    ''' Make M3U playlist '''
    try:
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write('#EXTM3U\n')
            for media in files:
                file.write(f'../{media}\n')
    except FileNotFoundError:
        return False
    return True


def get_playlist_items(playlist_path: str | Path) -> list | None:
    ''' Return playlist content '''
    playlist = []

    if not Path(playlist_path).exists():
        return None

    try:
        with open(playlist_path, 'r', encoding='utf-8') as file:
            playlist = file.read().splitlines()

        # Remove M3U header
        playlist.pop(0)

        # Remove path
        for i, item in enumerate(playlist):
            playlist[i] = Path(item).name
    except OSError:
        pass
    return playlist
