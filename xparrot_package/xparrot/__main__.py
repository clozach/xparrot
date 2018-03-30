# -*- coding: utf-8 -*-
"""
xParrot-cli provides a simple interface for interacting with the xParrot self-cleaning "todo list".

You'll need to set `AIRTABLE_API_KEY` in your environment for now. (I wasn't able to figure out a way to launch in interactive mode with a pre-launch variable, so this, sadly, doesn't work: `xparrot -i -k keyXXXXxxxXXX`.

Usage:
    xparrot (-i | --interactive)
    xparrot tasks [--sort_by <sort_description>]
    xparrot projects [--sort_by <sort_description>] [--include_tasks] 


Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --version    Show version.

Powered by docopt. (See simpler example at <project_root>/components_cookbook/interactive_cli.py.)
"""
import cmd
import sys
import json
from .xparrot_api import xParrotAPI as x
from .xparrot_api import tasks_ready_to_be_moved_to_archive
from .helpers.docopt_helpers import docopt_cmd, docopt


def isNotEmpty(
        s
):  #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return bool(s and s.strip())


class xparrot(cmd.Cmd):
    intro = 'Welcome to xParrot, the stiffest todo' \
        + ' list this side of the River Styx!' \
        + ' (type help for a list of commands.)'
    prompt = '🐦 § '
    file = None

    @docopt_cmd
    def do_tasks(self, arg):
        """Prints out all tasks.
        Usage: tasks [--sort_by <sort_description>]
                
        Options:
            -i, --interactive  Interactive Mode
            -h, --help  Show this screen and exit.
        """
        response = x().fetch(tasks_ready_to_be_moved_to_archive())
        tasks = next(response)
        if (tasks is None) or (len(tasks) == 0):
            print("No tasks to auto-archive. 😎")
            return [], []
        else:
            for task in tasks:
                print("\n", json.dumps(task, indent=4), "\n")

    @docopt_cmd
    def do_projects(self, arg):
        """Usage: projects [--sort_by <sort_description>] [--include_tasks]"""
        print("\nARGS\n", arg, "\n")

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('💀 🐦🥊 ❧ .  .    .       .             .                 .')
        exit()

    def do_q(self, arg):
        """Alias for `quit`."""
        xparrot.do_quit(self, arg)


cli_args = docopt(__doc__, sys.argv[1:])
print(cli_args)
if cli_args['--interactive']:
    xparrot().cmdloop()
