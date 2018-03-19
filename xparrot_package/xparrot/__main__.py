"""xParrot.

Usage:
  xParrot list [ (--todo | --tasks) | --projects | --subprojects ] [ --sort (byExpectedStart | byStatus) ] [ --group (byProject | bySubproject | byStatus) ]
  xParrot list
  xParrot sayHi <name>
  xParrot (-h | --help)
  xParrot --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
# todo: add [--filter] or summat to `list` command
from docopt import docopt
from .xparrot_api import xParrotAPI as x
from .funcmodule import dummy_print


def isNotEmpty(
        s
):  #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return bool(s and s.strip())


def main():
    args = docopt(__doc__, version='xParrot 0.0.0')
    print(args)

    if args['sayHi'] and isNotEmpty(args['<name>']):
        dummy_print('Yo {}!'.format(args['<name>']))
    elif args['list']:
        response = x("<your_airtable_api_key>").fetch(
            "OR({Status}='Done',{Status}='Auto-archived')")
        print(response)
        tasks = next(response)
        if (tasks is None) or (len(tasks) == 0):
            print("No tasks to auto-archive. 😎")
            return [], []
        else:
            for task in tasks:
                print("🌊 🌊 🌊")
                print(task)
                print("🌊 🌊 🌊")

    else:
        print(
            "Actually, with the current help def, docopt won't even let us get this far. 😎"
        )


if __name__ == '__main__':
    main()