#! /usr/bin/env python3
"""
## Command ``syn``

Searches for all synonyms of the word given in parameter (french). See `syn --help` for more details.

### Example

```
$ # searches for all synonyms of 'gentil'
$ syn gentil
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
    url_crisco = 'http://www.crisco.unicaen.fr/des/synonymes/{}'
    url = url_crisco.format(word)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table')
    if table is None:
        print('Nothing found...')
        return
    syns = table.find_all('a', attrs={"href": re.compile(r'des/synonymes/*')})
    syns_txt = [syn.text.replace(u'\xa0', u'') for syn in syns]
    print_list(syns_txt)

if __name__ == "__main__":
    main()
