#! /usr/bin/env python3
"""
    The ``_srl`` module
    ===================
    Contains all the functions related to the SRL ("set", "delete" and "list") commands.
"""

import click
from ._json import *

def decorate_srl(f):
    return click.option('--assign', '-a', help='Assign a value to the given key.', default=None,)(
    click.option('--delete', '-d', help='Delete a key.', is_flag=True,)(
    click.option('--list', '-l', help='List all the keys if no given key. Otherwise print the associated value.', is_flag=True,)(
    click.option('--set_datafile', '-s', help='Set considered datafile for this command.', default=None,)(
    f))))

def handle_srl(command, filename, keys, assign = None, delete = None, list = None, set_datafile = None, type = None):
    if assign is not None:
        if len(keys)!=1:
            print("When setting a new value, you should provide exactly one key.")
            exit()
        if type in ['dir','file']:
            assign = resolve_path(assign)
            if type=='dir' and len(assign)>=2 and assign[-2:] in ["\\.","/."]:
                assign = assign[:-2]
        set_json(filename, {keys[0]: assign})
        return True

    if delete:
        remove_json(filename, keys)
        return True

    if list:
        list_json(filename, keys)
        return True

    if set_datafile is not None:
        if len(keys)>0:
            print('Should not provide any key when setting a new datafile')
            exit()
        set_config(command, set_datafile)
        return True

    return False

def resolve_path(set):
    if os.path.exists(set):
        if not os.path.isabs(set):
            set = os.path.join(os.getcwd(),set)
    else:
        exit("Given file not found. Aborting.")
    return set
