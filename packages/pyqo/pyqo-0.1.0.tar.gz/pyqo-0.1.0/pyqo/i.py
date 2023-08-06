#! /usr/bin/env python3
"""
## Command ``i``

Open your favourite websites with ease. See `i --help` for more details.

### Example

```
$ # associate permanently the key 'github' to 'http://www.github.com'
$ i github -a http://www.github.com
$ # associate permanently the key 'so' to 'https://stackoverflow.com/'
$ i so -a https://stackoverflow.com/
$ # open the two websites on the existing webbrowser window
$ i github so
$ # open github and performs a google search for 'python' on a new webbrowser window
$ i -n github -g python
```
"""

import click
import sys, os
from ._json import *
from ._srl import *
from ._webbrowser import open_new, open_new_tab
from urllib.parse import quote

@click.command()
@click.argument('keys', required = False, nargs=-1)
@click.option('--new_window', '-n', help='Open results in a new window.', is_flag=True,)
@click.option('--google', '-g', help='Perform a google search.', multiple=True)
@click.option('--youtube', '-y', help='Perform a youtube search.', multiple=True)
@decorate_srl
def main(keys, new_window, google, youtube, **kwargs):
    """Open websites."""

    command = 'i'
    filename = resolve_json_filename(command)

    if handle_srl(command, filename, keys, **kwargs):
        return

    value_keys = get_json(filename, keys)

    google_url = 'https://www.google.com/search?q={}'
    value_google = [google_url.format(quote(r)) for r in google]

    youtube_url = 'https://www.youtube.com/results?search_query={}'
    value_youtube = [youtube_url.format(quote(r)) for r in youtube]

    urls = value_keys + value_google + value_youtube
    if len(keys)==0 and len(google)==0 and len(youtube)==0:
        urls = ['https://www.google.com']

    for i in range(len(urls)):
        if i == 0 and new_window:
            open_new(urls[i])
        else:
            open_new_tab(urls[i])

if __name__ == "__main__":
    main()
