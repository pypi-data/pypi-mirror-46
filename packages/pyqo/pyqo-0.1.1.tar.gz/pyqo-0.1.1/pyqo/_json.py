#! /usr/bin/env python3
"""
    The ``._json`` module
    ======================
    Contains all the functions related to the reading and mofifications of the ``.json`` files
"""

import json
import os
import sys

PYTHON_PATH = os.path.dirname(os.path.realpath(__file__))
HOME_PATH = os.path.expanduser('~')
CONFIG_PATH = os.path.join(HOME_PATH,'.config')
DATA_PATH = os.path.join(CONFIG_PATH, 'pyqo')

def resolve_json_filename(command):
    if not os.path.isdir(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
    if not os.path.isdir(DATA_PATH):
        os.mkdir(DATA_PATH)
    #init default filename
    filename = os.path.join(DATA_PATH,'{}.json'.format(command))
    #test if config
    config = read_json(os.path.join(DATA_PATH,'config.json'))
    key_name = '{}_json'.format(command)
    if key_name in config:
            filename = config[key_name]

    return filename

def set_config(command, datafile):
    config_file = os.path.join(DATA_PATH,'config.json')
    key_name = '{}_json'.format(command)
    data = read_json(config_file)
    data[key_name] = datafile
    write_json(config_file, data)

def read_json(filename):
    if os.path.isfile(filename):
        with open(filename, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = {}
    return data

def list_json(filename, keys):
    from ._printer import print_map
    if keys is None or len(keys)<1 or keys[0] is None:
        data = read_json(filename)
        print_map(data)
    else:
        values = get_json(filename, keys)
        dico = {keys[i] : values[i] for i in range(len(keys))}
        print_map(dico)

def get_json(filename, keys):
    data = read_json(filename)
    l = []
    for key in keys:
        if key in data:
            l.append(data[key])
        else:
            print('The key "{}" has no attributed value.'.format(key))
            del key
    return l

def write_json(filename, data):
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(data, f)

def set_json(filename, map):
    data = read_json(filename)
    for key, value in map.items():
        data[key] = value
    write_json(filename, data)

def remove_json(filename, keys):
    data = read_json(filename)
    for key in keys:
        data.pop(key)
    write_json(filename, data)
