import json
from pathlib import Path


def load_json(file_path: str | Path) -> dict | None:
    ''' Load JSON file '''
    try:
        return json.loads(Path(file_path).read_text('utf-8'))
    except FileNotFoundError:
        return None


def save_json(file_path: str | Path, data: dict):
    ''' Save JSON to a file '''
    Path(file_path).write_text(json.dumps(data), 'utf-8')


def save_json_key(file_path: str | Path, key: str, value: any):
    ''' Save JSON key '''
    json_file = load_json(file_path)
    json_file[key] = value
    save_json(file_path, json_file)


def update_vars(file_path: str, var_dict: dict):
    ''' Find and replace variable value in script file '''
    data = None
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    for i, line in enumerate(data):
        for var, val in var_dict.items():
            if var in line:
                data[i] = f'{var}{val}\n'

    with open(file_path, 'w', encoding='utf-8', newline='\n') as file:
        file.writelines(data)
