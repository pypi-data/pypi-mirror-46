#! /usr/bin/env python3
"""
    The ``._printer`` module
    =======================
    Contains all functions whose purpose is to display results of this library.
"""

WIDTH = 19
PER_LINE = 4

def print_list(datas):
    r = ""
    for idx,data in enumerate(sorted(datas)):
        r+="{d:<{width}}".format(d=data, width=WIDTH)
        if (idx+1)%PER_LINE == 0:
            r+="\n"
    print(r)

def print_map(datas):
    for key, value in datas.items():
        print('{key:<{width}}: {value}'.format(key=key, width=WIDTH, value=value))
