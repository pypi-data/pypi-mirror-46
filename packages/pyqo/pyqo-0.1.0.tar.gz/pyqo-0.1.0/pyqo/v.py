#! /usr/bin/env python3
"""
## Command ``v``

Associative table to save small variables. See `v --help` for more details.

### Example

```
$ # save the value '+44 1234 123456' under the key 'john_number'
$ v john_number -a '+44 1234 123456'
$ # print John's number
$ v john_number
$ # forget John's number
$ v john_number -r
```
"""

import click
import sys, os
from ._json import *
from ._srl import *

@click.command()
@click.argument('keys', required = False, nargs=-1)
@decorate_srl
def main(keys, **kwargs):
    """Contains variables."""
    
    command = 'v'
    filename = resolve_json_filename(command)

    if handle_srl(command, filename, keys, **kwargs):
        return

    values = get_json(filename, keys)
    for value in values:
        print(value)

if __name__ == "__main__":
    main()
