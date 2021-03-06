# -*- coding: utf-8 -*-
"""
xParrot-cli provides a simple interface for interacting with the xParrot self-cleaning "todo list".

You'll need to set `AIRTABLE_API_KEY` in your environment for now. (I wasn't able to figure out a way to launch in interactive mode with a pre-launch variable, so this, sadly, doesn't work: `xparrot -i -k keyXXXXxxxXXX`.

Usage:
    xparrot (-i | --interactive)
    xparrot tasks [--sort-by=<sort_description>] [--started | --stale | --done | --autodone | --endangered | --expired]
    xparrot projects [--sort-by <sort_description>] [--include-tasks] 
    xparrot subprojects [--sort-by <sort_description>] [--include-tasks] 
    xparrot task (--id <record-id> | --name <name>)

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
from .helpers.xparrot_api_helpers import print_tasks, print_task, print_projects, print_subprojects


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
        """Prints out tasks.
        📝 --sort-by NYI. The default filter is Unstarted. "All" is not currently an option.

        Usage: tasks [--sort-by <sort_description>] [--started | --stale | --done | --autodone | --endangered | --expired]
                
        Options:
            -i, --interactive  Interactive Mode
            -h, --help  Show this screen and exit.
        """
        if (arg['--started']):
            response = x().fetch(xPF.started())
        elif (arg['--stale']):
            response = x().fetch(xPF.stale())
        elif (arg['--done']):
            response = x().fetch(xPF.done())
        elif (arg['--autodone']):
            response = x().fetch(xPF.auto_archived())
        elif (arg['--endangered']):
            response = x().fetch(xPF.endangered())
        elif (arg['--expired']):
            response = x().fetch(xPF.expired())
        else:
            response = x().fetch(xPF.unstarted())
        print_tasks(response)

    @docopt_cmd
    def do_projects(self, arg):
        """Usage: projects [--sort-by <sort_description>] [--include-tasks]"""
        response = x().fetch_projects()
        print_projects(response)

    @docopt_cmd
    def do_subprojects(self, arg):
        """Prints out 
        Usage: subprojects [--sort-by <sort_description>] [--include-tasks]"""
        response = x().fetch_subprojects()
        print_subprojects(response)

    @docopt_cmd
    def do_task(self, arg):
        """Usage: task (--id <record-id> | --name <name>)"""
        if (arg['--id']):
            task_id = arg['<record-id>']
            try:
                response = x().task(task_id)
                print_task(response)
            except Exception as e:
                print('⚠️ ', e)
        elif (arg['--name']): # 🙀 Only works for task names without spaces
            task_name = arg['<name>']
            print('👗 Looking up Task "', task_name, '"')
            response = x().fetch(xPF.by_name(task_name))
            print_tasks(self, response)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('💀 🐦🥊 ❧ .  .    .       .             .                 .')
        exit()

    def do_q(self, arg):
        """Alias for `quit`."""
        xparrot.do_quit(self, arg)


cli_args = docopt(__doc__, sys.argv[1:])
if cli_args['--interactive']:
    xparrot().cmdloop()
