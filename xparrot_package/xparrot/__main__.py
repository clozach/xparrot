"""xParrot.

Usage:
  xparrot list [(-k <airtable_api_key> | --key_to_airtable_api <airtable_api_key>)] [(--todo | --tasks) | --projects | --subprojects ] [ --sort (byExpectedStart | byStatus) ] [ --group (byProject | bySubproject | byStatus) ]
  xparrot list [(-k <airtable_api_key> | --key_to_airtable_api <airtable_api_key>)]
  xparrot sayHi <name>
  xparrot (-h | --help)
  xparrot --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
# todo: add [--filter] or summat to `list` command
import os
from docopt import docopt
from .xparrot_api import xParrotAPI as x
from .xparrot_api import ready_for_archive
from .funcmodule import dummy_print


def isNotEmpty(
        s
):  #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return bool(s and s.strip())


def main():
    args = docopt(__doc__, version='xParrot 0.0.0')
    print(args)

    if isNotEmpty(args['<airtable_api_key>']):
        api_key = args['<airtable_api_key>']
    else:
        api_key = os.environ['AIRTABLE_API_KEY']

    if not isNotEmpty(api_key):
        print(
            'API key missing. Please pass it in with `-k <your_airtable_api_key>` or `--key_to_airtable_api <your_airtable_api_key>`, or set the environment variable, `AIRTABLE_API_KEY`. Thank you.'
        )
    elif args['sayHi'] and isNotEmpty(args['<name>']):
        dummy_print('Yo {}!'.format(args['<name>']))
    elif args['list']:
        response = x(api_key).fetch(ready_for_archive())
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