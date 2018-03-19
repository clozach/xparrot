"""xParrot.

Usage:
  xParrot list
  xParrot sayHi <name>
  xParrot (-h | --help)
  xParrot --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from .classmodule import Yo
from .funcmodule import dummy_print


def isNotEmpty(
        s
):  #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return bool(s and s.strip())


def main():
    args = docopt(__doc__, version='cliapp 0.0.1')

    if args['sayHi'] and isNotEmpty(args['<name>']):
        Yo(args['<name>']).say_name()
    elif args['list']:
        dummy_print(['a', 'α', 'eh?'])
    else:
        print(
            "Actually, with the current help def, docopt won't even let us get this far. 😎"
        )


if __name__ == '__main__':
    main()