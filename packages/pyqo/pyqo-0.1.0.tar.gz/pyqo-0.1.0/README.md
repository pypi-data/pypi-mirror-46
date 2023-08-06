
# pyqo
A set of useful command line scripts to navigate through your files and directories, and to get informed quickly.

## Compatibility
Fully compatible with :

- **Windows** 7 and higher.
- **Linux** distributions running under the X Window System.

Requires `Python 3`. Tested on `Python 3.6`.

## Usage
Install the [PyPI package](https://pypi.python.org/pypi/pyqo/):
```
$ pip install pyqo
```
and you're ready to go.
You can also clone the repository:
```
$ git clone https://github.com/Whenti/pyqo
```
or [download and extract the zip](https://github.com/Whenti/pyqo/archive/master.zip), and then run the setup:
```
$ python setup.py install
```

Check the [commands documentation below](https://github.com/Whenti/pyqo#Commands) to see what is available.

## Dependencies
See the [requirements.txt](requirements.txt) file for details.

## Authors

* **Quentin LÉVÊQUE** - [Whenti](https://github.com/Whenti)

## License
This project is proudly licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

# Commands
Below we briefly describe the different commands of `pyqo`. Make sure to use the `--help` option for more details.


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

## Command ``ant``

Searches for all antonyms of the word given in parameter (french). See `ant --help` for more details.

### Example

```
$ # searches for all antonyms of 'gentil'
$ ant gentil
```

## Command ``syn``

Searches for all synonyms of the word given in parameter (french). See `syn --help` for more details.

### Example

```
$ # searches for all synonyms of 'gentil'
$ syn gentil
```

## Command ``say``

Launches a synthesized voice that reads the given parameters. See `say --help` for more details.

### Example

```
$ say "Hi, how are you ?"
```

## Command ``rand``

Display a random integer. See `rand --help` for more details.

### Example

```
$ # randomly draw an integer between 5 and 10
$ rand -m 5 -M 10
```

## Command ``yget``

Downloads in the current folder the youtube video whose url is passed as a parameter. See `yget --help` for more details.

### Example

```
$ # downloads the youtube video '"Sweet Victory" Performance'
$ yget https://www.youtube.com/watch?v=k9iYm9PEAHg
```

## Command ``define``

Searches for the definition of the word given in parameter (french). See `define --help` for more details.

### Example

```
$ # searches for the definition of 'gentil'
$ define gentil
```