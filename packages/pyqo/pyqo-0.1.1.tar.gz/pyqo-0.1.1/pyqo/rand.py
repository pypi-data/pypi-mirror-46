#! /usr/bin/env python3
"""
## Command ``rand``

Display a random integer. See `rand --help` for more details.

### Example

```
$ # randomly draw an integer between 5 and 10
$ rand -m 5 -M 10
```
"""

import click
import random
import sys

@click.command()
@click.option('--min', '-m', help='minimum value', default=0,)
@click.option('--max', '-M', help='maximum value', default=6,)
def main(min, max):
    """Print a random number."""
    print(random.randint(min,max))

if __name__ == "__main__":
    main()
