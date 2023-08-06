#! /usr/bin/env python3
"""
## Command ``f``

Open your favourite files with ease. See `f --help` for more details.

### Example

```
$ cd ~
$ # associate permanently the key 'bashrc' to the file '~/.bashrc'
$ f bashrc -a .bashrc
$ cd ~/Documents/games
$ # open the '~/.bashrc' file
$ f bashrc
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
    """open directories"""

    command = 'f'
    filename = resolve_json_filename(command)

    if handle_srl(command, filename, keys, type='file', **kwargs):
        return

    files = get_json(filename, keys)

    cmd = 'xdg-open {}' if sys.platform in ['linux','linux2'] else 'start "" "{}"'
    for file in files:
        subprocess.call(cmd.format(file), shell=True, stderr=DEVNULL, stdout=DEVNULL)


if __name__ == "__main__":
    main()
