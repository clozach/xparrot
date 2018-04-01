# -*- coding: utf-8 -*-
"""
xParrot-cli provides a simple interface for interacting with the xParrot self-cleaning "todo list".

You'll need to set `AIRTABLE_API_KEY` in your environment for now. (I wasn't able to figure out a way to launch in interactive mode with a pre-launch variable, so this, sadly, doesn't work: `xparrot -i -k keyXXXXxxxXXX`.

Usage:
    xparrot (-i | --interactive)
    xparrot tasks [--sort_by=<sort_description>] [--started | --stale]
    xparrot projects [--sort_by <sort_description>] [--include_tasks] 


Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --version    Show version.

Powered by docopt. (See simpler example at <project_root>/components_cookbook/interactive_cli.py.)
"""
import cmd
import sys
from .xparrot_api import xParrotAPI as x
from .xparrot_api import xPF
from .helpers.docopt_helpers import docopt_cmd, docopt
from .helpers.xparrot_api_helpers import print_tasks


def isNotEmpty(
        s
):  #https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return bool(s and s.strip())


class xparrot(cmd.Cmd):
    intro = """Welcome to xParrot, the stiffest todo list this side of the River Styx!
(Type help for a list of commands.)"""
    prompt = '🐦 § '
    file = None

    @docopt_cmd
    def do_tasks(self, arg):
        """Prints out all tasks.
        Usage: tasks [--sort_by <sort_description>] [--started | --stale]
                
        Options:
            -i, --interactive  Interactive Mode
            -h, --help  Show this screen and exit.
        """
        if (arg['--started']):
            response = x().fetch(xPF.started())
        elif (arg['--stale']):
            response = x().fetch(xPF.stale())
        else:
            response = x().fetch(xPF.unstarted())
        print_tasks(self, response)

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
