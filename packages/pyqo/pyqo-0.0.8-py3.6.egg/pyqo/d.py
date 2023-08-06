#! /usr/bin/env python3
"""
## Command ``d``

Open the file manager to your favourite directories with ease.
The command `d` shares its data with the command `c`.
See `d --help` for more details.

### Example

```
$ cd ~/Documents/games
$ # open the current working directory, here '~/Documents/games'
$ d
$ # associate permanently the key 'films' to '~/Documents/films'
$ d films -a /home/pyqo/Documents/films
$ # open '~/Documents/films'
$ d films
```
"""
import click
import sys, os
from ._json import *
from ._srl import *
import subprocess
from subprocess import DEVNULL

@click.command()
@click.argument('keys', required = False, nargs=-1)
@decorate_srl

def main(keys, **kwargs):
    """Open directories."""
    command = 'd'
    filename = resolve_json_filename(command)

    if handle_srl(command, filename, keys, type='dir', **kwargs):
        return

    cmd = 'xdg-open {}' if sys.platform in ['linux','linux2'] else 'start "" "{}"'

    if len(keys)<1:
        dirs = [os.getcwd()]
    else:
        dirs = get_json(filename, keys)

    for dir in dirs:
        subprocess.call(cmd.format(dir), shell=True, stderr=DEVNULL, stdout=DEVNULL)

if __name__ == "__main__":
    main()
