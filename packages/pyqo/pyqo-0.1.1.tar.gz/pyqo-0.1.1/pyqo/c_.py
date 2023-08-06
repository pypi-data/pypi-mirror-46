#! /usr/bin/env python3
"""
## Command ``c``

Set the working directory of the command line to your favourite directories with ease.
For a script to alter the current environment, it requires `source`'ing in linux.
We suggest you to create an alias to avoid doing it manually : `alias c="source c"`.
The command `c` shares its data with the command `d`.
See `c --help` for more details.

### Example

```
$ cd ~/Documents/games
$ # associate permanently the key 'games' to '~/Documents/games'
$ c games -a .
$ # associate permanently the key 'films' to '~/Documents/films'
$ c films -a /home/pyqo/Documents/films
$ # equivalent to 'cd ~/Documents/films'
$ c films
$ # equivalent to 'cd ~/Documents/games'
$ c games
```
"""

import click
import sys, os
from ._json import *
from ._srl import *

@click.command()
@click.argument('keys', required = False, nargs = -1)
@decorate_srl
def main(keys, **kwargs):
    """Navigate through directories."""

    command = 'd'
    filename = resolve_json_filename(command)

    if handle_srl(command, filename, keys, type='dir', **kwargs):
        exit()

    if len(keys)!=1:
        print("When changing directory, you should provide exactly one key.")
        exit()

    values = get_json(filename, keys)

    if len(values)<1:
        print("Key not known, aborting.")
        exit()
    ret = values[0] if sys.platform in ['linux','linux2'] else '"'+values[0]+'"'
    exit(ret)

if __name__ == "__main__":
    main()
