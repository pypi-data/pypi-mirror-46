#! /usr/bin/env python3
"""
## Command ``ant``

Searches for all antonyms of the word given in parameter (french). See `ant --help` for more details.

### Example

```
$ # searches for all antonyms of 'gentil'
$ ant gentil
```
"""

import click
from bs4 import BeautifulSoup
import requests
import re
from ._printer import print_list
from urllib.parse import quote

@click.command()
@click.argument('word')
def main(word):
    """Retrieve synonyms."""
    url_antonyme = 'http://www.antonyme.org/antonyme/{}'
    url = url_antonyme.format(quote(word))

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    fiche = soup.find('div', attrs={"class": "fiche"})
    table = fiche.find('ul', attrs={"class": "synos"})
    if table is None:
        print('Nothing found...')
        return
    syns = table.find_all('a', attrs={"href": re.compile(r'http://www.antonyme.org/antonyme/*')})
    syns_txt = [syn.text.replace(u'\xa0', u'') for syn in syns]

    print_list(syns_txt)

if __name__ == "__main__":
    main()
