#! /usr/bin/env python3
"""
## Command ``say``

Launches a synthesized voice that reads the given parameters. See `say --help` for more details.

### Example

```
$ say "Hi, how are you ?"
```
"""


import click
import sys, os
import pyttsx3

@click.command()
@click.argument('speech', nargs=-1)
def main(speech):
    """Simulate the reading of the given speech."""
    engine = pyttsx3.init()
    for word in speech:
        engine.say(speech)
    engine.runAndWait()

if __name__ == "__main__":
    main()
