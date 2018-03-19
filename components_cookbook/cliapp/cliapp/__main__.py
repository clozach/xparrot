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


def main():
    arguments = docopt(__doc__, version='cliapp 0.0.1')

    print(arguments)


if __name__ == '__main__':
    main()