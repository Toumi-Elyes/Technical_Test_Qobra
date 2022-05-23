import json

def open_json_file(filepath: str):
    '''
    Open json file and set content in python dict.

    :param filepath: name and path of the file.
    :return: dict with the json file content.
    '''

    with open(filepath) as f:
        data = json.load(f)
        return data

def write_json_file(filepath: str, data: dict, indent: int):
    '''
    Create json file and Write into it.

    :param filepath: name and path of the file.
    :param data: content that will be loaded in the file.
    :param indent: number of space to indent file content.
    :return: dict with the json file content.
    '''

    with open(filepath, 'w') as f:
        json.dump(data, f, indent = indent)