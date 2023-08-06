#! /usr/bin/env python3
"""
## Command ``yget``

Downloads in the current folder the youtube video whose url is passed as a parameter. See `yget --help` for more details.

### Example

```
$ # downloads the youtube video '"Sweet Victory" Performance'
$ yget https://www.youtube.com/watch?v=k9iYm9PEAHg
```
"""

import click
import pytube
import sys
import os

@click.command()
@click.argument('url')
def main(url):
    """Download the youtube video in the current directory."""

    print("Downloading {}".format(url))
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.first()
        stream.download(os.getcwd())
    except Exception as e:
        print(e)
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
